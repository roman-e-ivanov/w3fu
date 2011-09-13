from w3fu.web.base import Response
from w3fu.web.resources import Route, Resource
from w3fu.resources.middleware.context import user
from w3fu.resources.middleware.transform import xml


class Index(Resource):

    route = Route('/')

    @xml('index-html.xsl')
    @user()
    def get(self, app, req):
        return Response(200, {})
