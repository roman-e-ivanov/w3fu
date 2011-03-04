from w3fu import config
from w3fu.res.middleware import Middleware
from w3fu.storage import StorageError


class Storage(Middleware):

    def _handler(self, res, req, handler):
        res.db = res.app.storage.pull()
        try:
            return handler(res, req)
        except StorageError as e:
            return req.response(503, str(e))
        finally:
            res.app.storage.push(res.db)


class Logged(Middleware):

    def _handler(self, res, req, handler):
        res.user = None
        try:
            session_id = req.cookie[config.session_name].value
            session = res.db.sessions.find(session_id).fetch()
            if session:
                res.user = res.db.users.find(session['user_id']).fetch()
        except KeyError:
            pass
        resp = handler(res, req)
        if res.user is not None and resp.status == 200:
            resp.content['user'] = res.user
        return resp
