from w3fu.http import Response
from w3fu.resources import Middleware


class user(Middleware):

    def __init__(self, required=False):
        self._required = required

    def _handler(self, res, ctx, handler):
        user = ctx.state['user']
        if self._required and user is None:
            return Response.forbidden()
        resp = handler(res, ctx)
        if user is not None and resp.status == 200:
            resp.content['user'] = user
        return resp
