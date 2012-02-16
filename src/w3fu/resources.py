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
            return Response(405)
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

    def __init__(self, fs, strict=False):
        self.data = {}
        self.errors = {}
        self._unpack(self._decode(fs), strict)

    def dump(self, format=None):
        return {'data': self.data, 'errors': self.errors}

    def query(self):
        return self._encode(self._pack())

    def _pack(self):
        packed = {}
        for name, value in self.data.iteritems():
            self.args[name].pack(value, packed)
        return packed

    def _unpack(self, packed, strict):
        for name, arg in self.args.iteritems():
            try:
                self.data[name] = arg.unpack(packed)
            except ArgAbsentError as e:
                if strict:
                    self.errors[name] = e
                else:
                    self.data[name] = None
            except ArgError as e:
                self.errors[name] = e

    def _encode(self, packed):
        return urlencode([(k, v.encode('utf-8'))
                          for k, v in packed.iteritems()])

    def _decode(self, fs):
        return dict([(k, fs.getfirst(k).decode('utf-8'))
                     for k in fs.keys()])
