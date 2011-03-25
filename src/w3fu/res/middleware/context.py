from w3fu import config
from w3fu.res.middleware import Middleware
from w3fu.domain.auth import User, Session


class storage(Middleware):

    def _handler(self, res, req, handler):
        res.db = res.app.storage.pull()
        try:
            return handler(res, req)
        finally:
            res.app.storage.push(res.db)


class user(Middleware):

    def _handler(self, res, req, handler):
        res.user = None
        try:
            session_id = req.cookie[config.session_name].value
            session = Session.find(res.db, session_id)
            if session:
                res.user = User.find(session.user_id)
        except KeyError:
            pass
        resp = handler(res, req)
        if res.user is not None and resp.status == 200:
            resp.content['user'] = res.user
        return resp
