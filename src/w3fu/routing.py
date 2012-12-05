from re import compile
from urlparse import urlunsplit

from w3fu.http import NotFound, ServiceUnavailable
from w3fu.args import ArgError


class Router(object):

    def __init__(self, **routes):
        self._routes = routes
        self._routes_sorted = sorted(routes.itervalues(), reverse=True)

    def __getitem__(self, name):
        return self._routes[name]

    def __call__(self, req):
        for route in self._routes_sorted:
            resp = route(req)
            if resp is not None:
                return resp
        raise NotFound


class Route(object):

    def __init__(self, pattern, scheme='http', **args):
        self.pattern = pattern
        self._scheme = scheme
        self._args = args
        self._compile()
        self.target = None

    def __cmp__(self, other):
        return cmp(self.pattern, other.pattern)

    def __call__(self, req):
        args = self._match(req.path)
        if args is None:
            return None
        if self.target is None:
            raise ServiceUnavailable
        return self.target(req, **args)

    def url(self, req, query='', **args):
        return urlunsplit((self._scheme, req.host, self.path(**args),
                           query, ''))

    def path(self, **args):
        return self.pattern.format(**self._pack(args))

    def _match(self, path):
        match = self._re.match(path)
        return self._unpack(match.groupdict()) if match else None

    def _compile(self):
        args_pattern = dict((k, '(?P<{0}>{1})'.format(k, v.pattern()))
                       for k, v in self._args.iteritems())
        self._re = compile('^' + self.pattern.format(**args_pattern) + '$')

    def _unpack(self, packed):
        unpacked = {}
        for name, arg in self._args.iteritems():
            try:
                unpacked[name] = arg.unpack(packed)
            except ArgError:
                return None
        return unpacked

    def _pack(self, unpacked):
        packed = {}
        for name, arg in self._args.iteritems():
            arg.pack(unpacked[name], packed)
        return packed
