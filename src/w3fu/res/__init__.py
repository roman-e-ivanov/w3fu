from re import compile
from urlparse import urlunsplit
from urllib import urlencode

from w3fu import config
from w3fu.web import Response


def bind(pattern, *args, **kwargs):
    def f(cls):
        cls.pattern = pattern
        rargs = tuple('({0})'.format(v) for v in args)
        rkwargs = dict((k, '(?P<{0}>{1})'.format(k, v))
                         for k, v in kwargs.iteritems())
        cls.cpattern = compile('^{0}$'.format(pattern.format(*rargs, **rkwargs)))
        return cls
    return f


class Controller(object):

    def __init__(self, resources):
        self._resources = resources

    def dispatch(self, app, req):
        for rescls in self._resources:
            match = rescls.cpattern.match(req.path)
            if match:
                req.args = match.groupdict()
                return rescls(app).run(req)
        return Response(404)


OVERLOADABLE = frozenset(('put', 'delete'))


class Resource(object):

    _secure = False

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    @classmethod
    def url(cls, query={}, **kwargs):
        scheme = 'https' if cls._secure else 'http'
        path = cls.pattern.format(**kwargs)
        return urlunsplit((scheme, config.domain, path,
                           urlencode([(k, v.encode('utf-8'))
                                      for k, v in query.iteritems()]), ''))

    def __init__(self, app):
        self.app = app

    def run(self, req):
        method = req.method
        if method == 'post':
            overloaded = req.fs.getfirst('method')
            if overloaded in OVERLOADABLE:
                method = overloaded
        handler = getattr(self, method, None)
        if handler is None:
            return Response(405)
        return handler(req)
