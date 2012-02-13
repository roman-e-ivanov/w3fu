from re import compile
from urlparse import urlunsplit
from urllib import urlencode

from w3fu.web.base import Response


OVERLOADABLE = frozenset(['put', 'delete'])


class Controller(object):

    def __init__(self, context, resources):
        self.ctx = context
        self._resources = resources

    def dispatch(self, req):
        for res in self._resources:
            args = res.route.match(req.path)
            if args:
                req.args = args
                return res(req)
        return Response(404)


class Route(object):

    def __init__(self, pattern, scheme='http', *args, **kwargs):
        self._pattern = pattern
        self._scheme = scheme
        rargs = tuple('({0})'.format(v) for v in args)
        rkwargs = dict((k, '(?P<{0}>{1})'.format(k, v))
                         for k, v in kwargs.iteritems())
        self._cpattern = compile('^{0}$'.format(pattern.format(*rargs, **rkwargs)))

    def match(self, path):
        return self._cpattern.match(path)

    def url(self, req, query='', **kwargs):
        path = self._pattern.format(**kwargs)
        return urlunsplit((self._scheme, req.host, path, query, ''))


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
