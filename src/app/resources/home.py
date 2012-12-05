from w3fu.http import OK
from w3fu.resources import Resource, HTML

from app.view import blocks


class Home(Resource):

    html = HTML(blocks['pages/home'])

    @html.GET
    def get(self, req):
        return OK({})
