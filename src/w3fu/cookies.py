from datetime import datetime
from Cookie import Morsel

from w3fu.data.args import ArgError


def cookie_string(name, value, expires=None, path='/'):
    morsel = Morsel()
    morsel.set(name, value, str(value))
    morsel['path'] = path
    if expires is not None:
        morsel['expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
    return morsel.OutputString()


class CookieMeta(type):

    def __init__(cls, name, bases, attrs):
        cls.args = {}
        for name, attr in attrs.iteritems():
            if hasattr(attr, 'unpack'):
                cls.args[name] = attr
        super(CookieMeta, cls).__init__(name, bases, attrs)


class Cookie(object):

    __metaclass__ = CookieMeta

    @classmethod
    def attribute(cls, name, attr):
        if hasattr(attr, 'unpack'):
            cls.args[name] = attr

    def __init__(self, req):
        self._req = req

    def get(self, name):
        try:
            return self._req.ctx['cookie'][name]
        except KeyError:
            unpacked = self._unpack(name)
            self._req.ctx.setdefault('cookie', {})[name] = unpacked
            return unpacked

    def set(self, resp, name, value):
        arg = self.args[name]
        packed = {}
        arg.pack(value, packed)
        for k, v in packed.iteritems():
            cookie = cookie_string(k, v, datetime.utcnow() + arg.custom['ttl'])
            resp.header('Set-Cookie', cookie)

    def remove(self, resp, name):
        for field in self.args[name].fields():
            cookie = cookie_string(field, 0, datetime.utcfromtimestamp(0))
            resp.header('Set-Cookie', cookie)

    def _unpack(self, name):
        try:
            return self.args[name].unpack(self._req.cookie)
        except ArgError:
            return None
