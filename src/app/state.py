from datetime import datetime, timedelta

from w3fu.data.args import StrArg, ArgError

from app.storage.collections.auth import Users


class SessionState(object):

    _cookie = StrArg('u')
    _ttl = timedelta(days=1)

    def get(self, req):
        try:
            session_id = self._cookie.unpack(req.cookie)
        except ArgError:
            return None
        return session_id

    def set(self, resp, value):
        packed = {}
        self._cookie.pack(value, packed)
        for name, cookie in packed.iteritems():
            resp.set_cookie(name, cookie, datetime.utcnow() + self._ttl)

    def delete(self, resp):
        for field in self._cookie.fields():
            resp.set_cookie(field, 0, datetime.utcfromtimestamp(0))


class UserState(object):

    def __init__(self, ctx):
        self._users = Users(ctx.db)

    def get(self, req):
        session_id = req.ctx.state['session_id']
        if session_id is None:
            return None
        return self._users.find_valid_session(session_id, datetime.utcnow())
