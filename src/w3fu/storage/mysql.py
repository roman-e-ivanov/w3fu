import MySQLdb

from w3fu import config
from w3fu.storage import StorageError


class Query:

    def __init__(self, expr):
        self._p = 0
        self.params = {}
        self.pattern = self._and(expr)

    def _boolean(op):
        def func(self, e):
            return op.join('({0})'.format(getattr(self, '_' + k)(v))
                           for k, v in e.iteritems())
        return func

    _and = _boolean(' and ')
    _or = _boolean(' or ')

    def _cmp(op):
        def func(self, e):
            out = []
            for name, value in e.iteritems():
                self._p += 1
                key = 'p' + str(self._p)
                self.params[key] = value
                out.append('{0}{1}%({2})s'.format(name, op, key))
            return ' and '.join(out)
        return func

    _eq = _cmp('=')
    _ne = _cmp('!=')
    _gt = _cmp('>')
    _lt = _cmp('<')
    _gte = _cmp('>=')
    _lte = _cmp('<=')

    def _in(self, e):
        out = []
        for name, values in e.iteritems():
            keys = ['p' + str(p)
                    for p in range(self._p + 1, self._p + 1 + len(values))]
            self._p += len(values)
            self.params.update(dict(zip(keys, values)))
            out.append('{0} in ({1})'.format(name, ','.join('%({0})s'.format(k)
                                                            for k in keys)))
        return ' and '.join(out)


class Database(object):

    build_index_sql = 'insert ignore into {table}_{index} ({keys}) values ({values})'
    clear_index_sql = 'delete from {table}_{index} where id=%(id)s'
    insert_sql = 'insert ignore into {table} (data) values (%(data)s)'
    update_sql = 'update {table} set data=%(data)s where id=%(id)s'
    delete_sql = 'delete from {table} where id=%(id)s'
    select_sql = 'select id,data from {table} where id=%(id)s'
    count_sql = 'select count(id) from {table} where id=%(id)s'
    select_many_sql = 'select id,data from {table} where id in ({ids})'
    query_index_sql = 'select distinct id from {table}_{index} where {where}{order}{limit}'
    count_index_sql = 'select count(id) from {table}_{index} where {where}'

    def __init__(self):
        self._connect()

    def _connect(self):
        try:
            self._conn = MySQLdb.connect(host=config.conn_host,
                                         db=config.conn_db,
                                         user=config.conn_user,
                                         passwd=config.conn_passwd,
                                         use_unicode=True,
                                         charset='utf8')
        except MySQLdb.DatabaseError as e:
            raise StorageError(e)

    def _cursor(self):
        try:
            return self._conn.cursor()
        except MySQLdb.OperationalError:
            self._connect()
            return self._conn.cursor()

    def commit(self):
        try:
            self._conn.commit()
        except MySQLdb.DatabaseError as e:
            raise StorageError(e)

    def rollback(self):
        try:
            self._conn.rollback()
        except MySQLdb.DatabaseError as e:
            raise StorageError(e)

    def insert(self, entity):
        sql = self.insert_sql.format(table=entity.name())
        cursor = self._conn.cursor()
        cursor.execute(sql, {'data': entity.dump()})
        entity.id = cursor.lastrowid
        self.build_index(entity)

    def update(self, entity):
        self.clear_index(entity.__class__, entity.id)
        sql = self.update_sql.format(table=entity.name())
        cursor = self._conn.cursor()
        cursor.execute(sql, {'id': entity.id, 'data': entity.dump()})
        self.build_index(entity)

    def delete(self, cls, id):
        self.clear_index(cls, id)
        sql = self.delete_sql.format(table=cls.name())
        cursor = self._conn.cursor()
        cursor.execute(sql, {'id': id})

    def select(self, cls, id):
        sql = self.select_sql.format(table=cls.name())
        cursor = self._conn.cursor()
        cursor.execute(sql, {'id': id})
        row = cursor.fetchone()
        if row is None:
            return None
        (id, data) = row
        return cls(id, cls.load(data))

    def count(self, cls, id):
        sql = self.count_sql.format(table=cls.name())
        cursor = self._conn.cursor()
        cursor.execute(sql, {'id': id})
        return cursor.fetchone()[0]

    def select_many(self, cls, ids, sort=False):
        sql = self.select_many_sql.format(table=cls.name(),
                                          ids=','.join(['%s'] * len(ids)))
        cursor = self._conn.cursor()
        cursor.execute(sql, tuple(ids))
        entities = {}
        for id, data in cursor:
            entities[id] = cls(id, cls.load(data))
        if sort:
            return [entities[id] for id in ids]
        else:
            return entities.values()

    def build_index(self, entity):
        cursor = self._conn.cursor()
        for name, func in entity.index.iteritems():
            for index in func(entity):
                index['id'] = entity.id
                sql = self.build_index_sql.format(table=entity.name(), index=name,
                                                  keys=','.join(index.keys()),
                                                  values=','.join('%({0})s'.format(k)
                                                                  for k in index.keys())
                                                  )
                cursor.execute(sql, index)

    def clear_index(self, cls, id):
        cursor = self._conn.cursor()
        for name in cls.index.keys():
            sql = self.clear_index_sql.format(table=cls.name(), index=name)
            cursor.execute(sql, {'id': id})

    def query_index(self, cls, expr, sort=None, count=None, offset=0, index='index'):
        query = Query(expr)
        order = '' if sort is None else ' order by ' + ','.join(sort)
        limit = '' if count is None else ' limit {0},{1}'.format(offset, count)
        sql = self.query_index_sql.format(table=cls.name(),
                                          index=index, where=query.pattern,
                                          order=order, limit=limit)
        cursor = self._conn.cursor()
        cursor.execute(sql, query.params)
        return [id for id, in cursor]

    def count_index(self, cls, expr, index='index'):
        query = Query(expr)
        sql = self.count_index_sql.format(table=cls.name(), index=index,
                                          where=query.pattern)
        cursor = self._conn.cursor()
        cursor.execute(sql, query.params)
        return cursor.fetchone()[0]

    def select_index(self, cls, expr, sort=None, count=None, offset=0, index='index'):
        ids = self.query_index(cls, expr, sort, count, offset, index)
        if not ids:
            return []
        return self.select_many(cls, ids, sort is not None)
