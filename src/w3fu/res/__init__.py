import re


def bind(pattern, **args):
    def f(cls):
        cls.pattern = pattern
        cls.cpattern = re.compile(('^%s$' % pattern)
                                  % dict((k, '(?P<%s>%s)' % (k, v))
                                         for k, v in args.iteritems()))
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
                return rescls(app, req).run()
        return req.response(404)


class Resource(object):

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    @classmethod
    def path(cls, args={}):
        return cls.pattern % args

    def __init__(self, app, req):
        self.app = app
        self.req = req

    def run(self):
        try:
            method = getattr(self, self.req.method)
        except AttributeError:
            return self.req.response(405)
        return method()
