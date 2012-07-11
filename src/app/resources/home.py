from w3fu.routing import Route

from app.resources import Resource


class Home(Resource):

    route = Route('/home')

    _block_path = 'pages/home'

    def get(self, ctx):
        if not self.rc.state['user']:
            return self._forbidden()
        return self._ok({})
