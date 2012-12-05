# -*- coding: utf-8 -*-
from w3fu.http import OK
from w3fu.resources import Resource, HTML, JSON

from app.view import blocks


class Test(Resource):

    html = HTML(blocks['pages/test'])
    json = JSON()

    @html.GET
    @json.GET
    def get(self, req):
        return OK({})
