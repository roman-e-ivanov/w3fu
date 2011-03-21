class Expression(object):

    def __init__(self, pattern, params={}, order=0):
        self.pattern = pattern
        self.params = params
        self.order = order

    def __eq__(self, other):
        params = self.params.copy()
        key = '{0}.{1}'.format(self.pattern, self.order)
        params[key] = other
        return Expression('{0}=%({1})s'.format(key), params, self.order + 1)

    def __and__(self, other):
        params = self.params.copy()
        params.update(other.params)
        return Expression('({0} and {1})'.format(self.pattern, other.pattern),
                          params, max(self.order, other.order) + 1)


class Property(object):

    def __init__(self, name=None, default=None):
        self._name = name
        self._default = default

    def attach(self, name, cls):
        if self._name is None:
            self._name = name

    def __get__(self, obj, owner):
        try:
            return obj[self._name]
        except KeyError:
            return self._default


class Column(Property):

    def __init__(self, name=None, pk=False, fk=False, auto=False):
        super(Column, self).__init__(name)
        self._pk = pk
        self._fk = fk
        self._auto = auto

    def attach(self, name, cls):
        super(Column, self).attach(name, cls)
        if not hasattr(cls, 'columns'):
            cls.columns = []
        cls.columns.append(self._name)
        if self._pk:
            cls.pk = self._name
        if self._fk:
            cls.fk = self._name
        if self._auto:
            cls.auto = self._name

    def __get__(self, obj, owner):
        if obj is None:
            return Expression('{0}.{1}'.format(owner.table(), self._name))
        super(Column, self).__get__(obj, owner)

    def __set__(self, obj, value):
        obj[self.column] = value
        try:
            obj.modified.add(self._name)
        except AttributeError:
            obj.modified = set([self._name])


class Join(Property):

    def __init__(self, childcls):
        super(Join, self).__init__(default=[])
        self._childcls = childcls

    def attach(self, name, cls):
        super(Join, self).attach(name, cls)
        if not hasattr(cls, 'join'):
            cls.join = {}
        cls.join[self._childcls] = self._name


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

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return None

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
    name = Property()


class Firm(Entity):

    id = Column(pk=True, auto=True)
    name = Column()
    tags = Join(Tag)
    services = Join(Service)


class Mapper(object):

    insert_sql = 'insert ignore into {table} ({keys}) values ({values})'
    update_sql = 'update {table} set {set} where {exp}'
    delete_sql = 'delete from {table} where {exp}'
    select_sql = 'select {columns} from {table}{join} where {exp}'

    def __init__(self, conn):
        self._conn = conn

    def insert(self, entity):
        sql = self.insert_sql.format(table=entity.table(),
                                     keys=','.join(entity.fields),
                                     values=','.join('%({0})s'.format(entity[f])
                                                     for f in entity.fields))
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
                                     exp=' and '.join('%0=%({0})s'.format(f)
                                                      for f in entity.pk))
        return self._conn.cursor().execute(sql, dict(entity))

    def delete(self, entitycls, exp):
        sql = self.delete_sql.format(table=entitycls.table(), exp=exp.pattern)
        return self._conn.cursor().execute(sql, exp.params)

    def select(self, entitycls, pattern='1', params={}):
        tree = [(None, entitycls)]
        for _, cls in tree:
            try:
                tree.extend(zip([cls] * len(cls.join), cls.join.keys()))
            except AttributeError:
                continue
        columns = [(cls, column) for _, cls in tree for column in cls.columns]
        join = ''.join([' left join {0} on ({0}.{1}={2}.{3})'.format(child.table(), child.fk, cls.table(), cls.pk)
                        for cls, child in tree[1:]])
        sql = self.select_sql.format(
                                     columns=','.join(['{0}.{1}'.format(cls.table(), column)
                                                       for cls, column in columns]),
                                     table=entitycls.table(),
                                     join=join,
                                     exp=pattern
                                     )
        cursor = self._conn.cursor()
        cursor.execute(sql, params)
        index = {}
        order = {}
        for row in cursor:
            temp = {}
            for value, (cls, column) in zip(row, columns):
                if value is None:
                    continue
                temp.setdefault(cls, cls())[column] = value
            for cls, entity in temp.iteritems():
                if entity[cls.pk] not in index.setdefault(cls, {}):
                    index[cls][entity[cls.pk]] = entity
                    order.setdefault(cls, []).append(entity)
        for cls, child in tree[1:]:
            for entity in order[child]:
                try:
                    index[cls][entity[child.fk]].setdefault(cls.join[child], []).append(entity)
                except KeyError:
                    continue
        return order.get(entitycls, [])


import MySQLdb


db = MySQLdb.connect(
                     host='localhost',
                     db='test',
                     user='root',
                     passwd='12345678',
                     use_unicode=True,
                     charset='utf8'
                     )

z = Mapper(db)
a = z.select(Firm)

from pprint import pprint
pprint(a)
