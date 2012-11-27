from datetime import datetime, timedelta

from w3fu.args import StrArg, ArgError

from app.storage.auth import User, Session


class UserState(object):

    _arg = StrArg('u')
    _ttl = timedelta(days=1)

    def __init__(self, attr_name):
        self._attr_name = attr_name

    def __get__(self, req, owner):
        value = self._compute(req)
        setattr(req, self._attr_name, value)
        return value

    @classmethod
    def _session_id(cls, req):
        try:
            return cls._arg.unpack(req.cookie)
        except ArgError:
            return None

    @classmethod
    def _write_cookie(cls, resp, value):
        packed = {}
        cls._arg.pack(value, packed)
        for name, cookie in packed.iteritems():
            resp.set_cookie(name, cookie, datetime.utcnow() + cls._ttl)

    @classmethod
    def _delete_cookie(cls, resp):
        for field in cls._arg.fields():
            resp.set_cookie(field, 0, datetime.utcfromtimestamp(0))

    @classmethod
    def login(cls, resp, user):
        session = Session.new()
        User.push_session(user, session)
        cls._write_cookie(resp, session.id)

    @classmethod
    def logout(cls, req, resp):
        session_id = cls._cookie.unpack(req.cookie)
        if session_id is not None:
            User.pull_session(req.session_id)
        cls._delete_cookie(resp)

    def _compute(self, req):
        session_id = self._arg.unpack(req.cookie)
        if session_id is None:
            return None
        return User.find_valid_session(session_id, datetime.utcnow())
