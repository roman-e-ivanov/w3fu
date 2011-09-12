from re import compile
from urlparse import urlunsplit
from urllib import urlencode

from w3fu import config
from w3fu.web.base import Response


OVERLOADABLE = frozenset(['put', 'delete'])


class Controller(object):

    def __init__(self, resources):
        self._resources = resources

    def dispatch(self, app, req):
        for res_cls in self._resources:
            args = res_cls.route.match(req.path)
            if args:
                req.args = args
                return res_cls(app, req).run(app, req)
        return Response(404)


class Route(object):

    def __init__(self, pattern, secure=False, *args, **kwargs):
        self._secure = secure
        self._pattern = pattern
        rargs = tuple('({0})'.format(v) for v in args)
        rkwargs = dict((k, '(?P<{0}>{1})'.format(k, v))
                         for k, v in kwargs.iteritems())
        self._cpattern = compile('^{0}$'.format(pattern.format(*rargs, **rkwargs)))

    def match(self, path):
        return self._cpattern.match(path)

    def url(self, query={}, **kwargs):
        scheme = 'https' if self._secure else 'http'
        path = self._pattern.format(**kwargs)
        return urlunsplit((scheme, config.domain, path,
                           urlencode([(k, v.encode('utf-8'))
                                      for k, v in query.iteritems()]), ''))


class Resource(object):

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    def __init__(self, app, req):
        self.app = app
        self.req = req

    def run(self, app, req):
        method = req.method
        if method == 'post':
            overloaded = req.fs.getfirst('method')
            if overloaded in OVERLOADABLE:
                method = overloaded
        handler = getattr(self, method, None)
        if handler is None:
            return Response(405)
        return handler(app, req)


class Middleware(object):

    def __call__(self, handler):
        def f(res, app, req):
            return self._handler(res, app, req, handler)
        return f
