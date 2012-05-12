import os

from w3fu.resources import Middleware
from w3fu.data.dumpers import JsonDumper, XmlDumper, prettify
from w3fu.templating import Block

from app import config


class json(Middleware):

    def __init__(self, format='json'):
        self._dumper = JsonDumper(format)

    def _handler(self, res, ctx, handler):
        resp = handler(res, ctx)
        if resp.status == 200:
            resp.content_type = 'application/json'
            resp.content = self._dumper.dump(resp.content).encode('utf-8')
        return resp


class xml(Middleware):

    def __init__(self, xslt=None, format='xml'):
        if xslt is not None:
            xslt = os.path.join(config.xsl_path, xslt)
        self._dumper = XmlDumper(format, xslt)

    def _handler(self, res, ctx, handler):
        resp = handler(res, ctx)
        if resp.status == 200:
            name = prettify(res.__class__.__name__)
            resp.content_type = 'application/xhtml+xml'
            resp.content = self._dumper.dump(resp.content, name,
                                             'no-xslt' in ctx.req.cookie)
        return resp


class block(Middleware):

    def __init__(self, name=None, format='raw'):
        self._dumper = Block(name) if name else None

    def _handler(self, res, ctx, handler):
        resp = handler(res, ctx)
        if resp.status == 200:
            resp.content_type = 'text/html'
            if self._dumper:
                content = self._dumper.render(resp.content)
            else:
                content = str(resp.content)
            resp.content = content.encode('utf-8')
        return resp
