from re import compile
from urlparse import urlunsplit

from w3fu.base import Response
from w3fu.data.args import ArgError


class Router(object):

    def __init__(self, resources):
        self._resources = resources

    def __call__(self, req):
        for res in self._resources:
            args = res.route.match(req.path)
            if args is None:
                continue
            req.ctx['args'] = args
            return res(req)
        return Response.not_found()


class Route(object):

    def __init__(self, pattern, scheme='http', **args):
        self.pattern = pattern
        self._scheme = scheme
        self._args = args
        self._compile()

    def url(self, req, query='', **args):
        return urlunsplit((self._scheme, req.host, self.path(**args),
                           query, ''))

    def path(self, **args):
        return self.pattern.format(**self._pack(args))

    def match(self, path):
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
