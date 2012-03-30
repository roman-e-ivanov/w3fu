class CacheHandler(object):

    def __init__(self, handler):
        self._handler = handler

    def __call__(self, req):
        resp = self._handler(req)
        resp.header('Cache-Control', 'no-cache, no-store, max-age=0')
        return resp
