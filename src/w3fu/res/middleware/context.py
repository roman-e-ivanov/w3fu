from datetime import datetime

from w3fu import config
from w3fu.res.middleware import Middleware
from w3fu.domain.auth import Session


class storage(Middleware):

    def _handler(self, res, req, handler):
        res.db = res.app.storage.pull()
        try:
            return handler(res, req)
        finally:
            res.app.storage.push(res.db)


class session(Middleware):

    def _handler(self, res, req, handler):
        res.session = None
        try:
            uid = req.cookie[config.session_name].value
            session = Session.find_valid_uid(res.db, uid=uid, time=datetime.utcnow())
            if session is not None:
                res.session = session
        except KeyError:
            pass
        resp = handler(res, req)
        if res.session is not None and resp.status == 200:
            resp.content['session'] = res.session
        return resp
