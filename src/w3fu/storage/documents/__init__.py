from time import mktime
from pymongo.dbref import DBRef

from w3fu.data.util import b64e


class DocumentMeta(type):

    def __init__(cls, name, bases, attrs):
        cls.props = {}
        for name, attr in attrs.iteritems():
            if hasattr(attr, 'dump'):
                cls.props[name] = attr
        super(DocumentMeta, cls).__init__(name, bases, attrs)


class Document(dict):

    __metaclass__ = DocumentMeta

    _indexes = []

    @classmethod
    def ensure_indexes(cls, storage):
        for index, kwargs in cls._indexes:
            cls._c(storage).ensure_index(index, **kwargs)

    @classmethod
    def new(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    @classmethod
    def _c(cls, storage):
        return storage.db[cls.name()]

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.ready = set()

    def dump(self, format):
        doc = {}
        for name, prop in self.props.iteritems():
            value = prop.dump(self, name, format)
            if value is not None:
                doc[name] = value
        return doc


class Property(object):

    def __init__(self, name, formats=None):
        self._name = name
        self._formats = None if formats is None else set(formats)

    def __get__(self, doc, owner):
        try:
            return doc[self._name]
        except KeyError:
            raise AttributeError

    def __set__(self, doc, value):
        doc[self._name] = value

    def dump(self, doc, name, format):
        if self._formats is not None and format not in self._formats:
            return None
        return self._dump(getattr(doc, name), format)

    def _dump(self, attr, format):
        return attr


class Identity(Property):

    def __init__(self, name='_id', formats=None):
        super(Identity, self).__init__(name, formats)

    def _dump(self, attr, format):
        return b64e(attr.binary)


class Timestamp(Property):

    def _dump(self, attr, format):
        return int(mktime(attr.timetuple()))


class Container(Property):

    def __init__(self, name, cls, formats=None):
        super(Container, self).__init__(name, formats)
        self._cls = cls

    def __get__(self, doc, owner):
        attr = super(Container, self).__get__(doc, owner)
        if self._name not in doc.ready:
            attr = self._wrap(doc, attr)
            self.__set__(doc, attr)
        return attr

    def __set__(self, doc, value):
        super(Container, self).__set__(doc, value)
        doc.ready.add(self._name)

    def _make_embedded(self, doc, value):
        embedded = self._cls(value)
        embedded.c = doc.c
        return embedded

    def _wrap(self, doc, attr):
        return self._make_embedded(doc, attr)

    def _dump(self, attr, format):
        return attr.dump(format)


class Reference(Container):

    def _wrap(self, doc, attr):
        return self._make_embedded(doc, doc.c.database.dereference(attr))

    def __set__(self, doc, value):
        super(Container, self).__set__(doc, DBRef(value.name(), value.id))


class ListContainer(Container):

    def _wrap(self, doc, attr):
        return [self._make_embedded(doc, v) for v in attr]

    def _dump(self, attr, format):
        return [doc.dump(format) for doc in attr]


class DictContainer(Container):

    def _wrap(self, doc, attr):
        return dict([(k, self._make_embedded(doc, v)) for k, v in attr])

    def _dump(self, attr, format):
        return dict([(k, doc.dump(format)) for k, doc in attr])
