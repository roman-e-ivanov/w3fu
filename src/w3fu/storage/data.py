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

    @classmethod
    def find(cls, db, id):
        q = db.query()
        found = db.select(cls, q(cls.pk) == id)
        return found[0] if found else None

    @classmethod
    def delete(cls, db, id):
        q = db.query()
        return db.delete(cls, q(cls.pk) == id)

    def insert(self, db):
        return db.insert(self)

    def update(self, db):
        return db.update(self)

    def _new(self):
        pass
