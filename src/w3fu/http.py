import re
from Cookie import SimpleCookie, CookieError, Morsel
from cgi import FieldStorage


FORMAT_BY_TYPE = {'text/html': 'html',
                  'application/json': 'json'}


class Request(object):

    _allowed_formats = frozenset(FORMAT_BY_TYPE.values())
    _path_re = re.compile('^(.+)\.(\w+)?$')

    def __init__(self, environ):
        self._env = environ
        self._parse_cookie()
        self._parse_fs()
        self._parse_path()
        self.formats = [self.path_format] if self.path_format else ['html']
        self.scheme = self._env.get('wsgi.url_scheme', 'http')
        self.host = self._env.get('HTTP_HOST', '')
        self.referer = self._env.get('HTTP_REFERER')
        self.method = self._env.get('REQUEST_METHOD', '')

    def __getitem__(self, name):
        try:
            return getattr(self, name)
        except AttributeError:
            raise KeyError

    def _parse_path(self):
        path = self._env.get('PATH_INFO', '')
        match = self._path_re.match(path)
        if match:
            path, fmt = match.groups([1, 2])
            if fmt in self._allowed_formats:
                self.path = path
                self.path_format = fmt
                return
        self.path = path
        self.path_format = None

    def _parse_cookie(self):
        try:
            cookie = SimpleCookie(self._env.get('HTTP_COOKIE'))
        except CookieError:
            cookie = {}
        self.cookie = dict((k, v.value) for k, v in cookie.iteritems())

    def _parse_fs(self):
        self.fs = FieldStorage(fp=self._env['wsgi.input'],
                               environ=self._env,
                               keep_blank_values=True)


class Response(object):

    def __init__(self, content=None, content_type=None):
        self.content_type = content_type
        self.content = content
        self.headers = []

    def __call__(self, start_response):
        if self.content is not None:
            self.header('Content-Type', self.content_type + '; charset=UTF-8')
        start_response(str(self.code) + ' ' + self.desc, self.headers)
        return [] if self.content is None else [self.content]

    def header(self, name, value):
        self.headers.append((name, value))
        return self

    def set_cookie(self, name, value, expires=None, path='/'):
        morsel = Morsel()
        morsel.set(name, value, str(value))
        morsel['path'] = path
        if expires is not None:
            morsel['expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
        self.header('Set-Cookie', morsel.OutputString())
        return self


class OK(Response):

    code = 200
    desc = 'OK'


class Redirect(Response, Exception):

    code = 302
    desc = 'Found'

    def __init__(self, url):
        super(Redirect, self).__init__()
        self.url = url
        self.header('Location', url)


class Error(Response, Exception): pass


class BadRequest(Error):

    code = 400
    desc = 'Bad Request'


class Forbidden(Error):

    code = 403
    desc = 'Forbidden'


class NotFound(Error):

    code = 404
    desc = 'Not Found'


class MethodNotAllowed(Error):

    code = 405
    desc = 'Method Not Allowed'


class Conflict(Error):

    code = 409
    desc = 'Conflict'


class UnsupportedMediaType(Error):

    code = 415
    desc = 'Unsupported Media Type'


class InternalServerError(Response, Exception):

    code = 500
    desc = 'Internal Server Error'


class ServiceUnavailable(Error):

    code = 503
    desc = 'Service Unavailable'


class Application(object):

    def __init__(self, handler):
        self._handler = handler

    def __call__(self, environ, start_response):
        try:
            resp = self._handler(Request(environ))
        except (Redirect, Error) as e:
            resp = e
        return resp(start_response)

    def debug(self, environ):
        def start_response(status, headers):
            print(status)
            for name, value in headers:
                print('{0}: {1}'.format(name, value))
        for data in self(environ, start_response):
            print
            print(data)
