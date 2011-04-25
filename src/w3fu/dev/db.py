from json import dumps, loads


class Entity(dict):

    index = {}

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    @classmethod
    def new(cls, *args, **kwargs):
        self = cls(cls._id(), cls._data())
        self.update(*args, **kwargs)
        return self

    @classmethod
    def _id(self):
        return None

    @classmethod
    def _data(self):
        return {}

    @classmethod
    def load(self, s):
        return loads(s)

    @classmethod
    def find(cls, db, id):
        return db.select(cls, id)

    def __init__(self, id, *args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)
        self.id = id

    def dump(self):
        return dumps(self, separators=(',', ':'))

    def put(self, db):
        return db.insert(self)

    def save(self, db):
        return db.update(self)


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
    insert_sql = 'insert ignore into {table} (id,data) values (%(id)s,%(data)s)'
    update_sql = 'update {table} set data=%(data)s where id=%(id)s'
    delete_sql = 'delete from {table} where id=%(id)s'
    select_sql = 'select id,data from {table} where id=%(id)s'
    select_many_sql = 'select id,data from {table} where id in ({ids})'
    query_index_sql = 'select distinct id from {table}_{index} where {where}{order}{limit}'
    count_index_sql = 'select count(id) from {table}_{index} where {where}'

    def __init__(self, conn):
        self._conn = conn

    def insert(self, entity):
        sql = self.insert_sql.format(table=entity.name())
        cursor = self._conn.cursor()
        cursor.execute(sql, {'id': entity.id, 'data': entity.dump()})
        rowcount = cursor.rowcount
        if entity.id is None:
            entity.id = cursor.lastrowid
        self.build_index(entity)
        return rowcount

    def update(self, entity):
        self.clear_index(entity.__class__, entity.id)
        sql = self.update_sql.format(table=entity.name())
        cursor = self._conn.cursor()
        cursor.execute(sql, {'id': entity.id, 'data': entity.dump()})
        rowcount = cursor.rowcount
        self.build_index(entity)
        return rowcount

    def delete(self, cls, id):
        self.clear_index(cls, id)
        sql = self.delete_sql.format(table=cls.name())
        cursor = self._conn.cursor()
        return cursor.execute(sql, {'id': id})

    def select(self, cls, id):
        sql = self.select_sql.format(table=cls.name())
        cursor = self._conn.cursor()
        cursor.execute(sql, {'id': id})
        row = cursor.fetchone()
        if row is None:
            return None
        (id, data) = row
        return cls(id, cls.load(data))

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
        sql = self.query_index_sql.format(table=cls.name(), index=index,
                                          where=query.pattern)
        cursor = self._conn.cursor()
        cursor.execute(sql, query.params)
        return cursor.fetchone()[0]

    def select_index(self, cls, expr=None, sort=None, count=None, offset=0,):
        ids = self.query_index(cls, index, expr, sort, count, offset)
        if not ids:
            return []
        return self.select_many(cls, ids, sort is not None)


class Firm(Entity):

    index = {
             'generic': lambda e: [{'f1': 1, 'f2': 2, 'f3': 3}],
             'special': lambda e: [
                                   {'f4': e['name']},
                                   {'f4': e['name']},
                                   {'f4': e['name']},
                                   {'f4': e['name']}
                                   ]
             }


import MySQLdb


conn = MySQLdb.connect(
                       host='localhost',
                       db='w3fu',
                       user='root',
                       passwd='12345678',
                       use_unicode=True,
                       charset='utf8'
                       )

from pprint import pprint

db = Database(conn)
#firm = Firm.new()
#firm['name'] = 'Google'
#firm['type'] = 10

firm = Firm.find(db, 1)
print(firm['name'])
firm['name'] = 'Yandex'
firm.save(db)
conn.commit()
