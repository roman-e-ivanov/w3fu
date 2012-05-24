from urllib import urlencode

from w3fu.base import Response
from w3fu.data.args import ArgError
from w3fu.data.codecs import json_dump


CONTENT_TYPES = {'html': 'text/html',
                 'json': 'application/json'}


class Resource(object):

    _block = None

    def __init__(self, ac, rc):
        self.ctx = ac
        self.ac = ac
        self.rc = rc
        self._template = ac.blocks[self._block] if self._block else None

    def __call__(self, ctx):
        self._format = 'html'
        handler = getattr(self, ctx.req.overriden_method.lower(), None)
        if handler is None:
            return Response.method_not_allowed()
        return handler(ctx)

    def _extra(self, data):
        pass

    def _render(self, data):
        if data is None:
            return ''
        self._extra(data)
        if self._format == 'html':
            if self._template is None:
                return str(data).encode('utf-8')
            else:
                return self._template.render(data).encode('utf-8')
        elif self._format == 'json':
            return json_dump(data)

    def _forbidden(self):
        return Response.forbidden()

    def _not_found(self):
        return Response.not_found()

    def _bad_request(self, data=None):
        if self._format == 'html':
            return Response.ok(self._render(data))
        else:
            return Response.bad_request()

    def _ok(self, data=None, redirect=None):
        if self._format == 'html' and redirect is not None:
            return Response.redirect(redirect)
        else:
            content_type = CONTENT_TYPES.get(self._format)
            return Response.ok(self._render(data), content_type=content_type)


class Middleware(object):

    def __call__(self, handler):
        def f(res, ctx):
            return self._handler(res, ctx, handler)
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

    def dump(self, private=True):
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
