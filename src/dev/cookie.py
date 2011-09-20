from base64 import b64encode, b64decode
from hashlib import sha1
from urllib import urlencode
from urlparse import parse_qsl
from uuid import uuid4


secret = 'f900101955b7481cb51c9b45badfc17d'

class Session(dict):

    def __init__(self, expires):
        super(Session, self).__init__()
        self.sid = uuid4().hex
        self.expires = expires
        self.modified = True

    def __setitem__(self, key, value):
        super(Session, self).__setitem__(key, value)
        self.modified = True

    def _signature(self, expires, sid, serialized):
        hasher = sha1()
        hasher.update('*'.join((sid, str(expires), secret)))
        k = hasher.hexdigest()
        hasher = sha1()
        hasher.update('*'.join((sid, str(expires), serialized, k)))
        return hasher.hexdigest()

    def load(self, cookie):
        p = cookie.split(':')
        if len(p) != 4 or self._signature(p[0], p[1], p[2]) != p[3]:
            return
        self.expires = p[0]
        self.sid = p[1]
        self.clear()
        self.update(dict(parse_qsl(p[2])))
        self.modified = False

    def dump(self):
        signature = self._signature(self.expires,
                                    self.sid,
                                    urlencode(self))
        cookie = ':'.join((str(self.expires),
                           self.sid,
                           urlencode(self),
                           signature))
        return cookie
        #return b64encode(cookie)
