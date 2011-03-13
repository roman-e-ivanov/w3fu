class Property(object):

    is_property = True

    def __init__(self, name, pk=False, auto=False):
        self.name = name
        self.pk = pk
        self.auto = auto

    def __get__(self, obj, cls):
        if obj is None:
            return self
        return obj[self._name]

    def __set__(self, obj, value):
        obj[self._name] = value
        try:
            obj.modified.add(self._name)
        except AttributeError:
            obj.modified = set([self._name])


class RowMeta(type):

    def __init__(cls, name, bases, attrs):
        cls.args = {}
        for name, attr in attrs.iteritems():
            if hasattr(attr, 'is_property'):
                cls.props.append = attr.name
                if attr.pk:
                    cls.pk.append = attr.name
                if attr.auto:
                    cls.auto = attr.name
        super(RowMeta, cls).__init__(name, bases, attrs)


class Row(dict):

    pk = []
    props = []
    join = []
    auto = None

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError

    @classmethod
    def new(cls, *args, **kwargs):
        self = cls(*args, **kwargs)
        self._new()
        return self

    def _new(self):
        pass
