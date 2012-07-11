from urllib import urlencode

from w3fu.http import Response
from w3fu.data.args import ArgError
from w3fu.util import json_dump


OVERLOADABLE = frozenset(['PUT', 'DELETE'])

CONTENT_TYPES = {'html': 'text/html',
                 'json': 'application/json'}


class BaseResource(object):

    _block_path = None
    _formats = ['html', 'json']

    def __init__(self, ctx):
        self._ctx = ctx
        if self._block_path:
            self._block = self._blocks.block(self._block_path)
        else:
            self._block = None

    def _content_type(self):
        return CONTENT_TYPES.get(self._format)

    def __call__(self, ctx):
        fmt = ctx.req.fs.getfirst('format')
        if fmt is None:
            self._format = self._formats[0]
        elif fmt in self._formats:
            self._format = fmt
        else:
            return Response.unsupported_media_type()
        method = ctx.req.method.lower()
        if method == 'POST':
            overloaded = ctx.req.fs.getfirst('method')
            if overloaded is not None and overloaded in OVERLOADABLE:
                method = overloaded
        handler = getattr(self, method, None)
        if handler is None:
            return Response.method_not_allowed()
        return handler(ctx)

    def _render(self, data):
        if data is None:
            return ''
        self._extra(data)
        if self._format == 'html':
            if self._block is None:
                return str(data).encode('utf-8')
            else:
                return self._block.render(data).encode('utf-8')
        elif self._format == 'json':
            return json_dump(data)

    def _forbidden(self):
        return Response.forbidden()

    def _not_found(self):
        return Response.not_found()

    def _conflict(self, data=None):
        content = self._render(data)
        content_type = self._content_type()
        if self._format == 'html':
            return Response.ok(content, content_type)
        else:
            return Response.conflict(content, content_type)

    def _bad_request(self, data=None):
        content = self._render(data)
        content_type = self._content_type()
        if self._format == 'html':
            return Response.ok(content, content_type)
        else:
            return Response.bad_request(content, content_type)

    def _ok(self, data=None, redirect=None):
        if self._format == 'html' and redirect is not None:
            return Response.redirect(redirect)
        else:
            return Response.ok(self._render(data), self._content_type())

    def _extra(self, data):
        pass


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

    def dump(self):
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
