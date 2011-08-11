from time import mktime

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

    @classmethod
    def ensure_indexes(cls, storage):
        pass

    @classmethod
    def new(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    @classmethod
    def c(cls, storage):
        return storage.db[cls.__name__.lower()]

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.ready = set()

    @property
    def id(self):
        return self['_id']

    @property
    def b64id(self):
        return b64e(self['_id'].binary)

    @property
    def ts(self):
        return self['_id'].generation_time

    def dump(self, format):
        doc = {} if self.get('_id') is None else {'id': self.b64id, 'ts': self.ts}
        for name, prop in self.props.iteritems():
            value = prop.dump(self, format)
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

    def dump(self, doc, format):
        if self._formats is not None and format not in self._formats:
            return None
        return getattr(doc, self._name)


class Container(Property):

    def __init__(self, name, cls, formats=None):
        super(Container, self).__init__(name, formats)
        self._cls = cls

    def __get__(self, doc, owner):
        attr = super(Container, self).__get__(doc, owner)
        if self._name not in doc.ready:
            for k, v in self._items(attr):
                attr[k] = self._cls(v)
            doc.ready.add(self._name)
        return attr

    def __set__(self, doc, value):
        super(Container, self).__set__(doc, value)
        doc.ready.add(self._name)


class ListContainer(Container):

    def _items(self, attr):
        return enumerate(attr)

    def dump(self, doc, format):
        attr = super(Container, self).dump(doc, format)
        if attr is None:
            return None
        return [doc.dump(format) for doc in attr]


class DictContainer(Container):

    def _items(self, attr):
        return attr.iteritems()

    def dump(self, doc, format):
        attr = super(Container, self).dump(doc, format)
        if attr is None:
            return None
        return dict([(key, doc.dump(format)) for key, doc in attr])
