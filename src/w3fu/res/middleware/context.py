from datetime import datetime

from w3fu import config
from w3fu.web import Response
from w3fu.res.middleware import Middleware


class storage(Middleware):

    def _handler(self, res, req, handler):
        try:
            return handler(res, req)
        finally:
            res.app.db.free()


class session(Middleware):

    def __init__(self, required=False):
        self._required = required

    def _handler(self, res, req, handler):
        req.session = None
        sid = req.cookie.get(config.session_name)
        if sid is not None:
            req.user = res.app.db.users.find_valid_session(sid.value,
                                                           datetime.utcnow())
        if self._required and req.session is None:
            return Response(403)
        resp = handler(res, req)
        if req.user is not None and resp.status == 200:
            resp.content['user'] = req.user
        return resp
