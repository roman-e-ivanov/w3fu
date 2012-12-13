from w3fu.http import OK
from w3fu.resources import Resource, HTML

from app.view import view
from app.mixins import public_mixins


class Index(Resource):

    html = HTML(view['pages/index'], public_mixins)

    @html.GET
    def get(self, req):
        return OK({})
