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

    is_property = True

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, owner):
        if obj is None:
            return Expression('{0}.{1}'.format(owner.table(), self.name))
        try:
            return obj[self.name]
        except KeyError:
            return None

    def __set__(self, obj, value):
        obj[self.name] = value
        try:
            obj.modified.add(self.name)
        except AttributeError:
            obj.modified = set([self.name])


class EntityMeta(type):

    def __init__(cls, name, bases, attrs):
        cls.props = []
        for name, attr in attrs.iteritems():
            if hasattr(attr, 'is_property'):
                cls.props.append(attr)
        super(EntityMeta, cls).__init__(name, bases, attrs)


class Entity(dict):

    __metaclass__ = EntityMeta

    pk = 'id'
    fk = 'owner'
    join = []
    auto = True

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

    id = Property('id')
    owner = Property('owner')
    value = Property('name')


class Service(Entity):

    id = Property('id')
    owner = Property('owner')
    name = Property('name')
    join = [Address]


class Tag(Entity):

    id = Property('id')
    owner = Property('owner')
    name = Property('name')


class Firm(Entity):

    id = Property('id')
    name = Property('name')
    join = [Tag, Service]


class Mapper(object):

    insert_sql = 'insert ignore into {table} ({keys}) values ({values})'
    update_sql = 'update {table} set {set} where {exp}'
    delete_sql = 'delete from {table} where {exp}'
    select_sql = 'select {fields} from {table}{join} where {exp}'

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
            tree.extend(zip([cls] * len(cls.join), cls.join))
        props = [(cls, prop) for _, cls in tree for prop in cls.props]
        fields = ','.join(['{0}.{1}'.format(cls.table(), prop.name)
                           for cls, prop in props])
        join = ''.join([' left join {0} on ({0}.{1}={2}.{3})'.format(this.table(), this.pk, child.table(), child.fk)
                        for this, child in tree[1:]])
        sql = self.select_sql.format(
                                     fields=fields,
                                     table=entitycls.table(),
                                     join=join,
                                     exp=pattern
                                     )
        print(sql)
        cursor = self._conn.cursor.execute(sql, params)
        if not cursor.rowcount:
            return []


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
z.select(Firm)
