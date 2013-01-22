from datetime import datetime, timedelta

from w3fu.http import Forbidden
from w3fu.args import StrArg, ArgError

from app.storage import users_c
from app.storage.auth import Session


class UserState(object):

    _arg = StrArg('u')
    _ttl = timedelta(days=1)

    def __init__(self, required=False):
        self._required = required

    def __call__(self, handler):
        def f(res, req, *args, **kwargs):
            if not hasattr(req, 'user'):
                session_id = self._read_cookie(req)
                if session_id is None:
                    req.user = None
                else:
                    req.user = users_c.find_valid_session(session_id,
                                                          datetime.utcnow())
            if self._required and req.user is None:
                raise Forbidden
            return handler(res, req, *args, **kwargs)
        return f

    @classmethod
    def _read_cookie(cls, req):
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
        users_c.push_session(user, session)
        cls._write_cookie(resp, session.id)

    @classmethod
    def logout(cls, req, resp):
        session_id = cls._read_cookie(req)
        if session_id is not None:
            users_c.pull_session(session_id)
        cls._delete_cookie(resp)
