from w3fu import http, routing, resources

from app.resources.middleware.transform import xml


class Debug(resources.Resource):

    route = routing.Route('/debug')

    @xml('pages/debug/html.xsl')
    def get(self, ctx):
        return http.Response.ok({})
