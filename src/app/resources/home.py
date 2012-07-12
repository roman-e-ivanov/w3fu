from w3fu.routing import Route

from app.view import templates
from app.resources import Resource


class Home(Resource):

    route = Route('/home')

    _block = templates.block('pages/home')

    def get(self, ctx):
        if not self.rc.state['user']:
            return self._forbidden()
        return self._ok({})
