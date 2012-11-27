from urllib import urlencode

from w3fu.args import ArgError
from w3fu.util import json_dump
from w3fu.http import OK, Error, Redirect, BadRequest, \
    UnsupportedMediaType, MethodNotAllowed


OVERLOADABLE = frozenset(['PUT', 'DELETE'])


class Resource(object):

    def __call__(self, req, **kwargs):
        for fmt in req.formats:
            try:
                renderer = getattr(self, fmt)
            except (KeyError, AttributeError):
                continue
            return renderer(self, req, **kwargs)
        raise UnsupportedMediaType


class Renderer(object):

    def __init__(self):
        self._handlers = {}

    def __getattr__(self, method):
        def decorator(f):
            self._handlers[method] = f
            return f
        return decorator

    def _handle(self, res, req, **kwargs):
        method = req.method
        if method == 'POST':
            overloaded = req.fs.getfirst('method')
            if overloaded is not None:
                if overloaded in OVERLOADABLE:
                    method = overloaded
                else:
                    raise MethodNotAllowed
        try:
            handler = self._handlers[method]
            return handler(res, req, **kwargs)
        except KeyError:
            raise MethodNotAllowed


class HTML(Renderer):

    def __init__(self, block=None, content_type='text/html'):
        super(HTML, self).__init__()
        self._block = block
        self._content_type = content_type

    def __call__(self, res, req, **kwargs):
        try:
            resp = self._handle(res, req, **kwargs)
            self._render(req, resp)
            return resp
        except Error as e:
            self._render(req, e)
            raise e

    def _render(self, req, resp):
        resp.content_type = self._content_type
        if resp.content is None:
            return
        if self._block is None:
            resp.content = str(resp.content).encode('utf-8')
        else:
            src = dict(req=req, **resp.content)
            resp.content = self._block.render('html', src).encode('utf-8')


class JSON(Renderer):

    def __init__(self, content_type='application/json', no_redirect=True):
        super(JSON, self).__init__()
        self._content_type = content_type
        self._no_redirect = no_redirect

    def __call__(self, res, req, **kwargs):
        try:
            resp = self._handle(res, req, **kwargs)
            self._render(req, resp)
            return resp
        except Error as e:
            self._render(req, e)
            raise e
        except Redirect as e:
            if self._no_redirect:
                resp = OK({'url': e.url})
                self._render(req, resp)
                return resp
            raise e

    def _render(self, req, resp):
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
    def handler(cls):
        def decorator(method):
            def f(res, req, **kwargs):
                req.form = cls(req)
                if req.form.errors:
                    raise BadRequest({})
                return method(res, req, **kwargs)
            return f
        return decorator

    def __init__(self, req):
        self.data = {}
        self.errors = {}
        self.src = self._decode(req.fs)
        self._unpack(self.src)

    def __getitem__(self, name):
        try:
            return getattr(self, name)
        except AttributeError:
            raise KeyError

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
