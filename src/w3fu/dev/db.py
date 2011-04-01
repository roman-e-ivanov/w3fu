from json import dumps, loads


class Entity(dict):

    indexes = []

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

    def __init__(self, id, *args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)
        self.id = id

    def dump(self):
        return dumps(self, separators=(',', ':'))


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


class Store(object):

    insert_sql = 'insert ignore into {table} (id,data) values (%(id)s,%(data)s)'
    update_sql = 'update {table} set data=%(data)s where id=%(id)s'
    select_sql = 'select id,data from {table} where id=%(id)s'
    delete_sql = 'delete from {table} where id=%(id)s'
    clear_index_sql = 'delete from {table}_{index} where id=%(id)s'
    build_index_sql = 'insert ignore into {table}_{index} ({keys}) values ({values})'
    select_index_sql = 'select distinct id from {table}_{index} {where}{order}{limit}'
    select_ids_sql = 'select id,data from {table} where id in ({ids})'

    def __init__(self, conn):
        self._conn = conn

    def build_index(self, entity):
        cursor = self._conn.cursor()
        for index, values in entity.index().iteritems():
            for value in values:
                value['id'] = entity.id
                sql = self.build_index_sql.format(table=entity.name(), index=index,
                                                  keys=','.join(values[0]),
                                                  values=','.join('%({0})s'.format(k)
                                                                  for k in values[0])
                                                  )
                print(sql)
                cursor.execute(sql, value)

    def clear_index(self, cls, id):
        cursor = self._conn.cursor()
        for index in cls.indexes:
            sql = self.clear_index_sql.format(table=cls.name(), index=index)
            print(sql)
            cursor.execute(sql, {'id': id})

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

    def select_index(self, cls, index, expr=None, sort=None, count=None, offset=0):
        if expr is None:
            where = ''
            params = None
        else:
            query = Query(expr)
            where = 'where ' + query.pattern
            params = query.params
        order = '' if sort is None else ' order by ' + ','.join(sort)
        limit = '' if count is None else ' limit {0},{1}'.format(offset, count)
        sql = self.select_index_sql.format(table=cls.name(), index=index,
                                           where=where, order=order, limit=limit)
        print(sql)
        cursor = self._conn.cursor()
        cursor.execute(sql, params)
        ids = [id for id, in cursor]
        sql = self.select_ids_sql.format(table=cls.name(),
                                         ids=','.join(['%s'] * len(ids)))
        print(sql)
        cursor.execute(sql, tuple(ids))
        entities = {}
        for id, data in cursor:
            entities[id] = cls(id, cls.load(data))
        if sort:
            return [entities[id] for id in ids]
        else:
            return entities.values()


class Firm(Entity):

    indexes = ['generic', 'special']

    def index(self):
        return {
                'generic': [{'f1': 1, 'f2': 2, 'f3': 3}],
                'special': [
                            {'f4': self['name']},
                            {'f4': self['name']},
                            {'f4': self['name']},
                            {'f4': self['name']}
                            ]
                }


import MySQLdb


db = MySQLdb.connect(
                     host='localhost',
                     db='w3fu',
                     user='root',
                     passwd='12345678',
                     use_unicode=True,
                     charset='utf8'
                     )

from pprint import pprint

s = Store(db)
firm = Firm.new()
firm['name'] = 'Google'
firm['type'] = 10
s.insert(firm)
db.commit()
