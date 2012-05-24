from w3fu.routing import Route

from app.resources.base import BaseResource


class Home(BaseResource):

    route = Route('/home')

    _block = 'pages/home'

    def get(self, ctx):
        if not self.rc.state['user']:
            return self._forbidden()
        return self._ok({})
