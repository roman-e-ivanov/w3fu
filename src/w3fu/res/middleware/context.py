from datetime import datetime

from w3fu import config
from w3fu.web import Response
from w3fu.res.middleware import Middleware
from w3fu.domain.auth import Session


class storage(Middleware):

    def _handler(self, res, req, handler):
        req.db = res.app.storage.pull()
        try:
            return handler(res, req)
        finally:
            res.app.storage.push(req.db)


class session(Middleware):

    def __init__(self, required=False):
        self._required = required

    def _handler(self, res, req, handler):
        req.session = None
        uid = req.cookie.get(config.session_name)
        if uid is not None:
            req.session = Session.find_valid_uid(req.db, uid=uid.value,
                                             time=datetime.utcnow())
        if self._required and req.session is None:
            return Response(403)
        resp = handler(res, req)
        if req.session is not None and resp.status == 200:
            resp.content['session'] = req.session
        return resp
