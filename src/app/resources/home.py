from w3fu.http import OK
from w3fu.routing import Route
from w3fu.resources import Resource, HTML

from app.view import blocks


class Home(Resource):

    route = Route('/home')

    html = HTML(blocks['pages/home'])

    @html.GET
    def get(self, ctx):
        return OK({})
