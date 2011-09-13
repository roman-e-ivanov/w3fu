from w3fu.web.base import Response
from w3fu.web.resources import Route, Resource
from w3fu.resources.middleware.context import user
from w3fu.resources.middleware.transform import xml


class Home(Resource):

    route = Route('/home')

    @xml('home-html.xsl')
    @user()
    def get(self, app, req):
        return Response(200, {})
