from datetime import datetime


class CacheHandler(object):

    def __init__(self, handler):
        self._handler = handler

    def __call__(self, req):
        resp = self._handler(req)
        resp.header('Cache-Control', 'no-cache, no-store, '
                    'must-revalidate, max-age=0')
        resp.header('Expires', datetime.utcfromtimestamp(0).strftime('%a, %d %b %Y %H:%M:%S GMT'))
        return resp
