from w3fu.http import OK
from w3fu.resources import Resource, HTML
from w3fu.util import class_wrapper

from app.view import view
from app.mixins import public_mixins
from app.state import UserState


@class_wrapper(UserState(True))
class Home(Resource):

    html = HTML(view['pages/home'], public_mixins)

    @html.GET
    def get(self, req):
        return OK({})
