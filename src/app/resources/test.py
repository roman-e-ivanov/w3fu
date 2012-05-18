# -*- coding: utf-8 -*-

from w3fu.base import Response
from w3fu.routing import Route
from w3fu.resources import Resource, Form
from w3fu.data.args import StrArg


class LoginForm(Form):

    email = StrArg('email', pattern=u'^[^@]+@[^@]+$',
                   min_size=4, max_size=254)

    password = StrArg('password', pattern=u'^[а-яА-Я\x21-\x7e]+$',
                      min_size=4, max_size=32)


class Test(Resource):

    route = Route('/test')

    _block = 'pages/test'

    def get(self, ctx):
        form = LoginForm(ctx.req)
        return self._ok({"form": form})
