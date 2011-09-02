from w3fu.res.middleware import Middleware
from w3fu.data.xml import to_xml
from w3fu.data._json import to_json


class json(Middleware):

    def __init__(self, format='xml'):
        self._format = format

    def _handler(self, res, app, req, handler):
        resp = handler(res, app, req)
        if resp.status == 200:
            resp.ctype = 'application/json'
            resp.content = to_json(resp.content, self._format).encode('utf-8')
        return resp


class xml(Middleware):

    def __init__(self, xslt=None, format='xml'):
        self._xslt = xslt
        self._format = format

    def _handler(self, res, app, req, handler):
        resp = handler(res, app, req)
        t = None if 'no-xslt' in req.fs else self._xslt
        ctype = 'application/xml' if t is None else 'text/html'
        if resp.status == 200:
            resp.ctype = ctype
            e = to_xml(res.name(), resp.content, self._format)
            resp.content = app.xslt.transform(e, t)
        return resp
