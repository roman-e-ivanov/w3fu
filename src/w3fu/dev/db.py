class Property(object):

    def __init__(self, name=None, default=None):
        self.name = name
        self._default = default

    def attach(self, name, cls):
        if self.name is None:
            self.name = name
        self.owner = cls

    def __get__(self, obj, cls):
        if obj is None:
            return self
        try:
            value = obj[self.name]
        except KeyError:
            return self._default
        try:
            return self._getter(obj, value)
        except AttributeError:
            return value

    def __set__(self, obj, value):
        try:
            obj[self.name] = self._setter(obj, value)
        except AttributeError:
            obj[self.name] = value
        try:
            obj.modified.add(self.name)
        except AttributeError:
            obj.modified = set([self.name])

    def getter(self, func):
        self._getter = func
        return func

    def setter(self, func):
        self._setter = func
        return func


class Column(Property):

    def __init__(self, name=None, pk=False, fk=False, auto=False):
        super(Column, self).__init__(name)
        self._pk = pk
        self._fk = fk
        self._auto = auto

    def attach(self, name, cls):
        super(Column, self).attach(name, cls)
        if not hasattr(cls, 'columns'):
            cls.columns = set()
        cls.columns.add(self.name)
        if self._pk:
            cls.pk = self
        if self._fk:
            cls.fk = self
        if self._auto:
            cls.auto = self


class Join(Property):

    def __init__(self, childcls):
        super(Join, self).__init__(default=[])
        self._childcls = childcls

    def attach(self, name, cls):
        super(Join, self).attach(name, cls)
        if not hasattr(cls, 'join'):
            cls.join = {}
        cls.join[self._childcls] = self.name


class EntityMeta(type):

    def __init__(cls, name, bases, attrs):
        for name, attr in attrs.iteritems():
            if hasattr(attr, 'attach'):
                attr.attach(name, cls)
        super(EntityMeta, cls).__init__(name, bases, attrs)


class Entity(dict):

    __metaclass__ = EntityMeta

    auto = None

    @classmethod
    def table(cls):
        return cls.__name__.lower()

    @classmethod
    def new(cls, *args, **kwargs):
        self = cls(*args, **kwargs)
        self._new()
        return self

    def _new(self):
        pass


class Address(Entity):

    id = Column(pk=True, auto=True)
    service_id = Column(fk=True)
    name = Column()


class Service(Entity):

    id = Column(pk=True, auto=True)
    firm_id = Column(fk=True)
    name = Column()
    addresses = Join(Address)


class Tag(Entity):

    id = Column(pk=True, auto=True)
    firm_id = Column(fk=True)
    name = Column()


class Firm(Entity):

    id = Column(pk=True, auto=True)
    name = Column()
    tags = Join(Tag)
    services = Join(Service)

    @name.getter
    def get_name(self, value):
        return value.lower()

    @name.setter
    def set_name(self, value):
        return value.upper()


class Query(object):

    def __init__(self, pattern, params={}):
        self.pattern = pattern
        self.params = params

    def _op(self, other, op):
        params = self.params.copy()
        params.update(other.params)
        return Query('({0} {1} {2})'.format(self.pattern, op, other.pattern), params)

    def __and__(self, other):
        return self._logical_op(other, 'and')


class PropertyQuery(object):

    _key = 0

    def __init__(self, property):
        self._pattern = '{0}.{1}'.format(property.owner.table(), property.name)

    def _op(self, other, op):
        self.__class__._key += 1
        key = 'p{0}'.format(self.__class__._key)
        return Query('{0}{1}%({2})s'.format(self._pattern, op, key), {key: other})

    def __eq__(self, other):
        return self._op(other, '=')


class Store(object):

    insert_sql = 'insert ignore into {table} ({keys}) values ({values})'
    update_sql = 'update {table} set {set} where {query}'
    delete_sql = 'delete from {table} where {query}'
    select_sql = 'select {columns} from {table}{join} where {query}'

    def __init__(self, conn):
        self._conn = conn

    def query(self):
        def make_query(property):
            return PropertyQuery(property)
        return make_query

    def insert(self, entity):
        sql = self.insert_sql.format(table=entity.table(),
                                     keys=','.join(entity.columns),
                                     values=','.join('%({0})s'.format(entity[f])
                                                     for f in entity.columns))
        cursor = self._conn.cursor()
        cursor.execute(sql, dict(entity))
        lastid = cursor.lastrowid
        if lastid and entity.auto is not None:
            entity[entity.auto] = lastid
        return cursor.rowcount

    def update(self, entity):
        sql = self.update_sql.format(table=entity.table(),
                                     set=','.join('{0}=%({0})s'.format(f)
                                                  for f in entity.modified),
                                     query=' and '.join('%0=%({0})s'.format(f)
                                                        for f in entity.pk))
        return self._conn.cursor().execute(sql, dict(entity))

    def delete(self, entitycls, exp):
        sql = self.delete_sql.format(table=entitycls.table(), exp=exp.pattern)
        return self._conn.cursor().execute(sql, exp.params)

    def select(self, entitycls, query=Query('1')):
        tree = [(None, entitycls)]
        for _, cls in tree:
            try:
                tree.extend(zip([cls] * len(cls.join), cls.join.keys()))
            except AttributeError:
                continue
        columns = [(cls, column) for _, cls in tree for column in cls.columns]
        join = ''.join([' left join {0} on ({0}.{1}={2}.{3})'.format(child.table(), child.fk.name, cls.table(), cls.pk.name)
                        for cls, child in tree[1:]])
        sql = self.select_sql.format(
                                     columns=','.join(['{0}.{1}'.format(cls.table(), column)
                                                       for cls, column in columns]),
                                     table=entitycls.table(),
                                     join=join,
                                     query=query.pattern
                                     )
        print(sql)
        cursor = self._conn.cursor()
        cursor.execute(sql, query.params)
        indexed = {}
        ordered = {}
        for row in cursor:
            temp = {}
            for value, (cls, column) in zip(row, columns):
                if value is None:
                    continue
                temp.setdefault(cls, cls())[column] = value
            for cls, entity in temp.iteritems():
                if entity[cls.pk.name] not in indexed.setdefault(cls, {}):
                    indexed[cls][entity[cls.pk.name]] = entity
                    ordered.setdefault(cls, []).append(entity)
        for cls, child in tree[1:]:
            try:
                for entity in ordered[child]:
                    indexed[cls][entity[child.fk.name]].setdefault(cls.join[child], []).append(entity)
            except KeyError:
                continue
        return ordered.get(entitycls, [])


import MySQLdb


db = MySQLdb.connect(
                     host='localhost',
                     db='test',
                     user='root',
                     passwd='12345678',
                     use_unicode=True,
                     charset='utf8'
                     )

from pprint import pprint

z = Store(db)
q = z.query()
a = z.select(Firm, q(Firm.pk) == 1)
pprint(a)
