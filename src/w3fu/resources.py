from urllib import urlencode

from w3fu.base import Response
from w3fu.data.args import ArgAbsentError, ArgError


OVERLOADABLE = frozenset(['put', 'delete'])


class Resource(object):

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    def __init__(self, context):
        self.ctx = context

    def __call__(self, req):
        method = req.method.lower()
        if method == 'post':
            overloaded = req.fs.getfirst('method')
            if overloaded in OVERLOADABLE:
                method = overloaded
        handler = getattr(self, method, None)
        if handler is None:
            return Response.method_not_allowed()
        return handler(req)


class Middleware(object):

    def __call__(self, handler):
        def f(res, req):
            return self._handler(res, req, handler)
        return f


class FormMeta(type):

    def __init__(cls, name, bases, attrs):
        cls.args = {}
        for name, attr in attrs.iteritems():
            if hasattr(attr, 'unpack'):
                cls.args[name] = attr
        super(FormMeta, cls).__init__(name, bases, attrs)


class Form(object):

    __metaclass__ = FormMeta

    @classmethod
    def attribute(cls, name, attr):
        if hasattr(attr, 'unpack'):
            cls.args[name] = attr

    def __init__(self, req):
        self.data = {}
        self.errors = {}
        self.src = self._decode(req.fs)
        self._unpack(self.src)

    def dump(self, format=None):
        return {'source': self.src, 'errors': self.errors}

    def query(self, **unpacked):
        packed = dict(self.src)
        packed.update(self._pack(unpacked))
        return self._encode(packed)

    def _pack(self, unpacked):
        packed = {}
        for name, value in unpacked.iteritems():
            self.args[name].pack(value, packed)
        return packed

    def _unpack(self, packed):
        for name, arg in self.args.iteritems():
            try:
                self.data[name] = arg.unpack(packed)
            except ArgError as e:
                self.errors[name] = e

    def _encode(self, packed):
        return urlencode([(k, v.encode('utf-8'))
                          for k, v in packed.iteritems()])

    def _decode(self, fs):
        return dict([(k, fs.getfirst(k).decode('utf-8'))
                     for k in fs.keys()])
