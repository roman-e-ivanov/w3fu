from datetime import datetime, timedelta

from w3fu.args import StrArg, ArgError

from app.storage.auth import User


class SessionIdState(object):

    _cookie = StrArg('u')
    _ttl = timedelta(days=1)

    def __get__(self, req, owner):
        value = self._value(req)
        req.session_id = value
        return value

    @classmethod
    def set(cls, resp, session_id):
        packed = {}
        cls._cookie.pack(session_id, packed)
        for name, cookie in packed.iteritems():
            resp.set_cookie(name, cookie, datetime.utcnow() + cls._ttl)

    @classmethod
    def delete(cls, resp):
        for field in cls._cookie.fields():
            resp.set_cookie(field, 0, datetime.utcfromtimestamp(0))

    def _value(self, req):
        try:
            return self._cookie.unpack(req.cookie)
        except ArgError:
            return None


class UserState(object):

    def __get__(self, req, owner):
        value = self._value(req)
        req.user = value
        return value

    def _value(self, req):
        if req.session_id is None:
            return None
        return User.find_valid_session(req.session_id, datetime.utcnow())
