class Middleware(object):

    def __call__(self, handler):
        def f(res, req):
            return self._handler(res, req, handler)
        return f
