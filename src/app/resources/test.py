# -*- coding: utf-8 -*-

from w3fu.routing import Route
from w3fu.resources import Form
from w3fu.data.args import StrArg

from app.resources.base import BaseResource


class LoginForm(Form):

    email = StrArg('email', pattern=u'^[^@]+@[^@]+$',
                   min_size=4, max_size=254)

    password = StrArg('password', pattern=u'^[а-яА-Я\x21-\x7e]+$',
                      min_size=4, max_size=32)


class Test(BaseResource):

    route = Route('/test')

    _block_path = 'pages/test'

    def get(self, ctx):
        form = LoginForm(ctx.req)
        return self._ok({'form': form})
