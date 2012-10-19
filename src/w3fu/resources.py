from urllib import urlencode

import w3fu.http as http
from w3fu.args import ArgError
from w3fu.util import json_dump


OVERLOADABLE = frozenset(['PUT', 'DELETE'])


class Resource(object):

    def __call__(self, ctx, **kwargs):
        for fmt in ctx.req.formats:
            try:
                renderer = getattr(self, fmt)
            except (KeyError, AttributeError):
                continue
            return renderer(self, ctx, **kwargs)
        raise http.UnsupportedMediaType


class Renderer(object):

    def __init__(self):
        self._handlers = {}

    def __getattr__(self, method):
        def decorator(f):
            self._handlers[method] = f
            return f
        return decorator

    def _handle(self, res, ctx, **kwargs):
        method = ctx.req.method
        if method == 'POST':
            overloaded = ctx.req.fs.getfirst('method')
            if overloaded is not None and overloaded in OVERLOADABLE:
                method = overloaded
        try:
            handler = self._handlers[method]
            return handler(res, ctx, **kwargs)
        except KeyError:
            raise http.MethodNotAllowed


class HTML(Renderer):

    def __init__(self, block=None, content_type='text/html'):
        super(HTML, self).__init__()
        self._block = block
        self._content_type = content_type

    def __call__(self, res, ctx, **kwargs):
        try:
            resp = self._handle(res, ctx, **kwargs)
            self._render(ctx, resp)
            return resp
        except http.Error as e:
            self._render(ctx, e)
            raise e

    def _render(self, ctx, resp):
        resp.content_type = self._content_type
        if resp.content is None:
            return
        if self._block is None:
            resp.content = str(resp.content).encode('utf-8')
        else:
            resp.content = self._block.render(resp.content).encode('utf-8')


class JSON(Renderer):

    def __init__(self, content_type='application/json', no_redirect=True):
        super(JSON, self).__init__()
        self._content_type = content_type
        self._no_redirect = no_redirect

    def __call__(self, res, ctx, **kwargs):
        try:
            resp = self._handle(res, ctx, **kwargs)
            self._render(ctx, resp)
            return resp
        except http.Error as e:
            self._render(ctx, e)
            raise e
        except http.Redirect as e:
            if self._no_redirect:
                resp = http.OK({'url': e.url})
                self._render(ctx, resp)
                return resp
            raise e

    def _render(self, ctx, resp):
        resp.content_type = self._content_type
        if resp.content is not None:
            resp.content = json_dump(resp.content)


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
