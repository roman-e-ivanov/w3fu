from urlparse import parse_qsl, urlunsplit
from urllib import urlencode
from Cookie import SimpleCookie, Morsel
from cgi import FieldStorage


class Application(object):

    def __init__(self, controller, storage, xslt):
        self.controller = controller
        self.storage = storage
        self.xslt = xslt

    def __call__(self, environ, start_response):
        req = Request(self, environ)
        resp = self.controller.dispatch(self, req)
        return resp.output(start_response)


class Request(object):

    def __init__(self, app, env):
        self.app = app
        self._env = env
        self.method = env.get('REQUEST_METHOD', '').lower()
        self.scheme = env.get('wsgi.url_scheme')
        self.host = env.get('HTTP_HOST')
        self.referer = env.get('HTTP_REFERER')
        self.path = env.get('PATH_INFO', '')
        self.cookie = SimpleCookie(env.get('HTTP_COOKIE', ''))
        self.fs = FieldStorage(fp=env['wsgi.input'], environ=env,
                               keep_blank_values=True)


STATUS_STRINGS = {
                  200: '200 OK',
                  301: '301 Moved Permanently',
                  302: '302 Found',
                  304: '304 Not Modified',
                  403: '404 Forbidden',
                  404: '404 Not Found',
                  405: '405 Method Not Allowed',
                  500: '500 Internal Server Error',
                  503: '503 Service Unavailable'
                  }


class Response(object):

    def __init__(self, status=200, content=None, ctype='text/plain'):
        self.status = status
        self.ctype = ctype
        self.content = content
        self.headers = []

    def output(self, start_response):
        if self.content is not None:
            self.header('Content-Type', self.ctype + '; charset=UTF-8')
        start_response(STATUS_STRINGS[self.status], self.headers)
        return [] if self.content is None else [self.content]

    def header(self, name, value):
        self.headers.append((name, value))
        return self

    def location(self, url):
        self.header('Location', url)
        return self

    def set_cookie(self, name, value, expires=None, path='/'):
        morsel = Morsel()
        morsel.set(name, value, str(value))
        morsel['path'] = path
        if expires is not None:
            morsel['expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
        self.header('Set-Cookie', morsel.OutputString())
        return self
