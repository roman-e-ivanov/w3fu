from pymongo import Connection
from pymongo.cursor import Cursor
from pymongo.errors import PyMongoError, AutoReconnect, DuplicateKeyError
from pymongo.dbref import DBRef
from copy import copy

from w3fu import util


class Database(util.RegistryMixin):

    def __init__(self, uri, dbname):
        self._connection = Connection(uri)
        self._db = self._connection[dbname]

    def collection(self, name):
        return self._db[name]

    def deref(self, ref):
        return self._db.dereference(ref)

    def free(self):
        self._connection.end_request()


def safe(wrap=False):
    def decorator(method):
        def handler(cls, *args, **kwargs):
            tried = False
            while True:
                try:
                    result = method(cls, *args, **kwargs)
                    if not wrap:
                        return result
                    if isinstance(result, Cursor):
                        return [cls(doc) for doc in result]
                    if result is not None:
                        return cls(result)
                    return None
                except AutoReconnect as e:
                    if tried:
                        raise StorageError(e)
                    tried = True
                except DuplicateKeyError:
                    return False
                except PyMongoError as e:
                    raise StorageError(e)
        return handler
    return decorator


class ModelMeta(type):

    def __init__(cls, name, bases, attrs):
        cls.props = {}
        for name, attr in attrs.iteritems():
            if hasattr(attr, 'dump'):
                cls.props[name] = attr
        super(ModelMeta, cls).__init__(name, bases, attrs)


class Model(object):

    __metaclass__ = ModelMeta

    _database = ''
    _collection = ''
    _indexes = []

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    @classmethod
    def _c(cls):
        return Database.pull(cls._database).collection(cls._collection)

    @classmethod
    @safe()
    def insert(cls, doc, safe=False):
        cls._c().insert(doc.raw, safe=safe)
        return True

    @classmethod
    @safe()
    def remove_id(cls, id, safe=False):
        return cls._c().remove({'_id': id}, safe=safe)

    @classmethod
    @safe(True)
    def find_id(cls, id):
        return cls._c().find_one({'_id': id})

    @classmethod
    def new(cls, *args, **kwargs):
        doc = cls({})
        doc._new(*args, **kwargs)
        return doc

    def __init__(self, raw, collection=None):
        self.raw = raw
        self.collection = collection
        self.containers = {}

    def _ensure_indexes(self):
        for index, kwargs in self._indexes:
            self._collection.ensure_index(index, **kwargs)

    def _new(self, *args, **kwargs):
        self.raw = dict(*args, **kwargs)

    def ref(self):
        return DBRef(self.collection.name(), self.id)

    def dump(self):
        doc = {}
        for name, prop in self.props.iteritems():
            value = prop.dump(self, name)
            if value is not None:
                doc[name] = value
        return doc

    def __getitem__(self, name):
        try:
            return getattr(self, name)
        except AttributeError:
            raise KeyError


class Property(object):

    def __init__(self, name, default=None, hidden=False):
        self._name = name
        self._default = default
        self._hidden = hidden

    def __get__(self, doc, owner):
        try:
            return doc.raw[self._name]
        except KeyError:
            doc.raw[self._name] = default = copy(self._default)
            return default

    def __set__(self, doc, value):
        doc.raw[self._name] = value

    def __delete__(self, doc):
        del doc.raw[self._name]

    def dump(self, doc, name):
        return None if self._hidden else self._dump(getattr(doc, name))

    def _dump(self, attr):
        return attr


class Container(Property):

    def __init__(self, name, cls, default={}, hidden=False):
        self._cls = cls
        super(Container, self).__init__(name, default, hidden)

    def __get__(self, doc, owner):
        try:
            attr = doc.containers[self._name]
        except KeyError:
            attr = self._wrap(doc, super(Container, self).__get__(doc, owner))
            self.__set__(doc, attr)
        return attr

    def __set__(self, doc, value):
        super(Container, self).__set__(doc, self._unwrap(value))
        doc.containers[self._name] = value

    def _wrap(self, doc, raw):
        return self._cls(doc.collection, raw)

    def _unwrap(self, doc):
        return doc.raw

    def _dump(self, doc):
        return doc.dump()


class Reference(Container):

    def _wrap(self, doc, raw):
        return self._cls(doc.collection, doc.collection.storage.deref(raw))

    def _unwrap(self, doc):
        return doc.ref()


class ListContainer(Container):

    def __init__(self, name, cls, hidden=False):
        super(ListContainer, self).__init__(name, cls, [], hidden)

    def _wrap(self, doc, raw):
        return [self._cls(doc.collection, v) for v in raw]

    def _unwrap(self, docs):
        return [doc.raw for doc in docs]

    def _dump(self, docs):
        return [doc.dump() for doc in docs]


class DictContainer(Container):

    def __init__(self, name, cls, hidden=False):
        super(DictContainer, self).__init__(name, cls, {}, hidden)

    def _wrap(self, doc, raw):
        return dict([(k, self._cls(doc.collection, v)) for k, v in raw.iteritems()])

    def _unwrap(self, docs):
        return dict([(k, doc.raw) for k, doc in docs.iteritems()])

    def _dump(self, docs):
        return dict([(k, doc.dump()) for k, doc in docs.iteritems()])


class StorageError(Exception): pass
