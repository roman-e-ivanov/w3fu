from datetime import datetime, timedelta

from w3fu.args import StrArg, ArgError
from w3fu.state import StateHandler

from app.storage.auth import User


class SessionState(object):

    _cookie = StrArg('u')
    _ttl = timedelta(days=1)

    def get(self, ctx):
        try:
            session_id = self._cookie.unpack(ctx.req.cookie)
        except ArgError:
            return None
        return session_id

    def set(self, ctx, resp, value):
        packed = {}
        self._cookie.pack(value, packed)
        for name, cookie in packed.iteritems():
            resp.set_cookie(name, cookie, datetime.utcnow() + self._ttl)

    def delete(self, ctx, resp):
        for field in self._cookie.fields():
            resp.set_cookie(field, 0, datetime.utcfromtimestamp(0))


class UserState(object):

    def get(self, ctx):
        session_id = ctx.state['session_id']
        if session_id is None:
            return None
        return User.find_valid_session(session_id, datetime.utcnow())


state = StateHandler(session_id=SessionState(), user=UserState())
