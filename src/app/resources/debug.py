from w3fu.http import Response
from w3fu.routing import Route
from w3fu.resources import Resource

from app.resources.middleware.transform import xml


class Debug(Resource):

    route = Route('/debug')

    @xml('pages/debug/html.xsl')
    def get(self, ctx):
        return Response.ok({})
