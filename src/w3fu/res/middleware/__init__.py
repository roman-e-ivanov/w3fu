class Middleware(object):

    def __call__(self, handler):
        def f(res, app, req):
            return self._handler(res, app, req, handler)
        return f
