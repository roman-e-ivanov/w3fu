from w3fu.data.util import b64e


class Document(dict):

    @classmethod
    def new(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.ready = set()

    @property
    def id(self):
        return self['_id']

    @property
    def id64(self):
        return self['_id']


class Property(object):

    def __init__(self, name):
        self._name = name

    def __get__(self, doc, owner):
        try:
            return doc[self._name]
        except KeyError:
            raise AttributeError

    def __set__(self, doc, value):
        doc[self._name] = value


class Container(Property):

    def __init__(self, name, cls=None):
        super(Container, self).__init__(name)
        self._cls = cls

    def __get__(self, doc, owner):
        attr = super(Container, self).__get__(doc, owner)
        if self._cls is not None and self._name not in doc.ready:
            try:
                items = attr.iteritems()
            except AttributeError:
                items = enumerate(attr)
            for k, v in items:
                attr[k] = self._cls(v)
            doc.ready.add(self._name)
        return attr

    def __set__(self, doc, value):
        super(Container, self).__set__(doc, value)
        doc.ready.add(self._name)
