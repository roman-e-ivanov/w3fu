from w3fu.base import Response
from w3fu.resources import Middleware


class user(Middleware):

    def __init__(self, required=False):
        self._required = required

    def _handler(self, res, req, handler):
        user = req.ctx.state['user']
        if self._required and user is None:
            return Response.forbidden()
        resp = handler(res, req)
        if user is not None and resp.status == 200:
            resp.content['user'] = user
        return resp
