from pymongo import Connection
from pymongo.cursor import Cursor
from pymongo.errors import PyMongoError, AutoReconnect, DuplicateKeyError
from copy import copy


def safe(wrap=False):
    def decorator(method):
        def handler(self, *args, **kwargs):
            tried = False
            while True:
                try:
                    result = method(self, *args, **kwargs)
                    if not wrap:
                        return result
                    if isinstance(result, Cursor):
                        return [self.document_cls(doc) for doc in result]
                    if result is not None:
                        return self.document_cls(result)
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


class StorageError(Exception): pass


class Database(object):

    def __init__(self, uri, dbname):
        self._connection = Connection(uri)
        self._db = self._connection[dbname]

    def collection(self, name):
        return self._db[name]

    def deref(self, ref):
        return self._db.dereference(ref)

    def free(self):
        self._connection.end_request()


class Collection(object):

    _indexes = []

    def __init__(self, db, name, document_cls=None):
        self._c = db.collection(name)
        self.document_cls = document_cls
        for index, kwargs in self._indexes:
            self._c.ensure_index(index, **kwargs)

    @safe()
    def insert(self, doc, safe=False):
        self._c.insert(doc.raw, safe=safe)
        return True

    @safe()
    def remove_id(self, _id, safe=False):
        return self._c.remove({'_id': _id}, safe=safe)

    @safe(True)
    def find_id(self, _id):
        return self._c.find_one({'_id': _id})


class DocumentMeta(type):

    def __init__(cls, name, bases, attrs):
        cls.props = {}
        for name, attr in attrs.iteritems():
            if hasattr(attr, 'dump'):
                cls.props[name] = attr
        super(DocumentMeta, cls).__init__(name, bases, attrs)


class Document(object):

    __metaclass__ = DocumentMeta

    @classmethod
    def new(cls, *args, **kwargs):
        doc = cls({})
        doc._new(*args, **kwargs)
        return doc

    def __init__(self, raw):
        self.raw = raw
        self.containers = {}

    def _new(self, *args, **kwargs):
        self.raw = dict(*args, **kwargs)

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
        return self._cls(raw)

    def _unwrap(self, doc):
        return doc.raw

    def _dump(self, doc):
        return doc.dump()


class ListContainer(Container):

    def __init__(self, name, cls, hidden=False):
        super(ListContainer, self).__init__(name, cls, [], hidden)

    def _wrap(self, doc, raw):
        return [self._cls(v) for v in raw]

    def _unwrap(self, docs):
        return [doc.raw for doc in docs]

    def _dump(self, docs):
        return [doc.dump() for doc in docs]


class DictContainer(Container):

    def __init__(self, name, cls, hidden=False):
        super(DictContainer, self).__init__(name, cls, {}, hidden)

    def _wrap(self, doc, raw):
        return dict([(k, self._cls(v)) for k, v in raw.iteritems()])

    def _unwrap(self, docs):
        return dict([(k, doc.raw) for k, doc in docs.iteritems()])

    def _dump(self, docs):
        return dict([(k, doc.dump()) for k, doc in docs.iteritems()])

