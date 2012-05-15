# -*- coding: utf-8 -*-

from w3fu.base import Response
from w3fu.routing import Route
from w3fu.resources import Resource

from app.resources.middleware.context import user
from app.resources.middleware.transform import block


class Test(Resource):

    route = Route('/test')

    @block('pages/test')
    def get(self, ctx):
        return Response.ok({"user": "John"})
