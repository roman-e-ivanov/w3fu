# -*- coding: utf-8 -*-
from w3fu.http import OK
from w3fu.routing import Route
from w3fu.resources import Resource, Form, HTML, JSON
from w3fu.args import StrArg

from app.view import blocks


class LoginForm(Form):

    email = StrArg('email', pattern=u'^[^@]+@[^@]+$',
                   min_size=4, max_size=254)

    password = StrArg('password', pattern=u'^[а-яА-Я\x21-\x7e]+$',
                      min_size=4, max_size=32)


class Test(Resource):

    route = Route('/test')

    html = HTML(blocks['pages/test'])
    json = JSON()

    @html.GET
    @json.GET
    def get(self, ctx):
        form = LoginForm(ctx.req)
        return OK({'form': form})
