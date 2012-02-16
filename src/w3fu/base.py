from Cookie import SimpleCookie, Morsel
from cgi import FieldStorage


STATUS_STRINGS = {200: '200 OK',
                  301: '301 Moved Permanently',
                  302: '302 Found',
                  304: '304 Not Modified',
                  403: '403 Forbidden',
                  404: '404 Not Found',
                  405: '405 Method Not Allowed',
                  500: '500 Internal Server Error',
                  503: '503 Service Unavailable'}


class Context(dict):

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value


class Application(object):

    def __init__(self, context, handler):
        self.ctx = context
        self._handler = handler

    def __call__(self, environ, start_response):
        req = Request(environ)
        resp = self._handler(req)
        return resp.output(start_response)

    def debug(self, environ):
        def start_response(status, headers):
            print(status)
            for name, value in headers:
                print('{0}: {1}'.format(name, value))
        for data in self(environ, start_response):
            print
            print(data)


class Request(object):

    def __init__(self, environ):
        self.environ = environ
        self.ctx = Context()

    @property
    def method(self):
        return self.environ.get('REQUEST_METHOD', '')

    @property
    def scheme(self):
        return self.environ.get('wsgi.url_scheme', 'http')

    @property
    def host(self):
        return self.environ.get('HTTP_HOST', '')

    @property
    def path(self):
        return self.environ.get('PATH_INFO', '')

    @property
    def cookie(self):
        try:
            return self._cookie
        except AttributeError:
            self._cookie = SimpleCookie(self.environ.get('HTTP_COOKIE', ''))
            return self._cookie

    @property
    def fs(self):
        try:
            return self._fs
        except AttributeError:
            self._fs = FieldStorage(fp=self.environ['wsgi.input'],
                                    environ=self.environ,
                                    keep_blank_values=True)
            return self._fs


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
