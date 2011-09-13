from w3fu.web.resources import Middleware
from w3fu.data.dumpers import JsonDumper, XmlDumper


class json(Middleware):

    def __init__(self, format='json'):
        self._dumper = JsonDumper(format)

    def _handler(self, res, app, req, handler):
        resp = handler(res, app, req)
        if resp.status == 200:
            resp.ctype = 'application/json'
            resp.content = self._dumper.dump(resp.content).encode('utf-8')
        return resp


class xml(Middleware):

    def __init__(self, xslt=None, format='xml'):
        self._dumper = XmlDumper(format, xslt)

    def _handler(self, res, app, req, handler):
        resp = handler(res, app, req)
        if resp.status == 200:
            resp.ctype = 'application/xhtml+xml'
            resp.content = self._dumper.dump(resp.content, res.name(),
                                        'no-xslt' in req.fs)
        return resp
