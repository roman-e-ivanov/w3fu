from w3fu.base import Response
from w3fu.routing import Route
from w3fu.resources import Resource

from app.resources.middleware.context import user
from app.resources.middleware.transform import xml


class Home(Resource):

    route = Route('/home')

    @xml('home-html.xsl')
    @user()
    def get(self, app, req):
        return Response(200, {})
