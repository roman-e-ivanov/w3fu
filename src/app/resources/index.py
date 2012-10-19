from w3fu.http import OK
from w3fu.routing import Route
from w3fu.resources import Resource, HTML

from app.view import blocks


class Index(Resource):

    route = Route('/')

    html = HTML(blocks['pages/index'])

    @html.GET
    def get(self, ctx):
        return OK({})
