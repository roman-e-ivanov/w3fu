from w3fu.routing import Route

from app.resources.base import BaseResource


class Index(BaseResource):

    route = Route('/')

    _block = 'pages/index'

    def get(self, ctx):
        return self._ok({})
