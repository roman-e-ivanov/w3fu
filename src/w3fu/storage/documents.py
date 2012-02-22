from pymongo.dbref import DBRef


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

    def __init__(self, raw, collection=None):
        self.raw = raw
        self.collection = collection
        self.containers = {}

    def _new(self, *args, **kwargs):
        self.raw = dict(*args, **kwargs)

    def ref(self):
        return DBRef(self.collection.name(), self.id)

    def dump(self, format):
        doc = {}
        for name, prop in self.props.iteritems():
            value = prop.dump(self, name, format)
            if value is not None:
                doc[name] = value
        return doc


class Property(object):

    listable = True

    def __init__(self, name, formats=None):
        self._name = name
        self._formats = None if formats is None else set(formats)

    def __get__(self, doc, owner):
        try:
            return doc.raw[self._name]
        except KeyError:
            raise AttributeError

    def __set__(self, doc, value):
        doc.raw[self._name] = value

    def dump(self, doc, name, format):
        if self._formats is not None and format not in self._formats:
            return None
        return self._dump(getattr(doc, name), format)

    def _dump(self, attr, format):
        return attr


class Container(Property):

    def __init__(self, name, cls, formats=None):
        super(Container, self).__init__(name, formats)
        self._cls = cls

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

    def _dump(self, doc, format):
        return doc.dump(format)


class Reference(Container):

    def _wrap(self, doc, raw):
        return self._cls(doc.collection, doc.collection.storage.deref(raw))

    def _unwrap(self, doc):
        return doc.ref()


class ListContainer(Container):

    def _wrap(self, doc, raw):
        return [self._cls(doc.collection, v) for v in raw]

    def _unwrap(self, docs):
        return [doc.raw for doc in docs]

    def _dump(self, docs, format):
        return [doc.dump(format) for doc in docs]


class DictContainer(Container):

    def _wrap(self, doc, raw):
        return dict([(k, self._cls(doc.collection, v)) for k, v in raw.iteritems()])

    def _unwrap(self, docs):
        return dict([(k, doc.raw) for k, doc in docs.iteritems()])

    def _dump(self, docs, format):
        return dict([(k, doc.dump(format)) for k, doc in docs.iteritems()])
