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
        res.session = None
        try:
            session_uid = req.cookie[config.session_name].value
            session = Session.find_valid_uid(res.db, session_uid)
            if session is not None:
                res.session = session
                res.user = User.find(res.db, session['user_id'])
        except KeyError:
            pass
        resp = handler(res, req)
        if res.user is not None and resp.status == 200:
            resp.content['user'] = res.user.dump()
        return resp
