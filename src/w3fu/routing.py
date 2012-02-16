from re import compile
from urlparse import urlunsplit

from w3fu.base import Response
from w3fu.data.args import ArgError


class Router(object):

    def __init__(self, resources):
        self._resources = resources

    def dispatch(self, req):
        for res in self._resources:
            args = res.route.match(req.path)
            if args:
                req.ctx['args'] = args
                return res(req)
        return Response(404)


class Route(object):

    def __init__(self, pattern, scheme='http', **args):
        self.pattern = pattern
        self._scheme = scheme
        self._args = args
        self._compile()

    def url(self, req, query='', **args):
        path = self.pattern.format(**self._pack(args))
        return urlunsplit((self._scheme, req.host, path, query, ''))

    def match(self, path):
        return self._re.match(path)

    def unpack(self, match):
        packed = match.groupdict()
        unpacked = {}
        for name, arg in self._args.iteritems():
            try:
                unpacked[name] = arg.unpack(packed)
            except ArgError:
                unpacked[name] = None
        return unpacked

    def _compile(self):
        args_re = dict((k, '(?P<{0}>{1})'.format(k, v.re()))
                       for k, v in self._args.iteritems())
        self._re = compile('^' + self.pattern.format(**args_re) + '$')

    def _pack(self, unpacked):
        packed = {}
        for name, arg in self._args.iteritems():
            arg.pack(unpacked[name], packed)
        return packed
