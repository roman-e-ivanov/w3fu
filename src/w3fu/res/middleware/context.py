from datetime import datetime

from w3fu import config
from w3fu.web import Response
from w3fu.res.middleware import Middleware
from w3fu.storage.documents.auth import User


class user(Middleware):

    def __init__(self, dump=None, required=False):
        self._dump = dump
        self._required = required

    def _handler(self, res, app, req, handler):
        req.user = None
        sid = req.cookie.get(config.session_name)
        if sid is not None:
            req.user = User.find_valid_session(app.storage, sid.value,
                                               datetime.utcnow())
        if self._required and req.session is None:
            return Response(403)
        resp = handler(res, app, req)
        if self._dump is not None and req.user is not None and resp.status == 200:
            resp.content['user'] = req.user.dump(self._dump)
        return resp
