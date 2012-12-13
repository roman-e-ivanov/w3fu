# -*- coding: utf-8 -*-
from w3fu.http import OK
from w3fu.resources import Resource, HTML, JSON

from app.view import view
from app.mixins import public_mixins


class Test(Resource):

    html = HTML(view['pages/test'], public_mixins)
    json = JSON()

    @html.GET
    @json.GET
    def get(self, req):
        return OK({})
