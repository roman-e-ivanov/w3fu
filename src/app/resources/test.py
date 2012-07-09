# -*- coding: utf-8 -*-

from w3fu import args, resources, routing

from app.resources.base import BaseResource


class LoginForm(resources.Form):

    email = args.StrArg('email', pattern=u'^[^@]+@[^@]+$',
                        min_size=4, max_size=254)

    password = args.StrArg('password', pattern=u'^[а-яА-Я\x21-\x7e]+$',
                           min_size=4, max_size=32)


class Test(BaseResource):

    route = routing.Route('/test')

    _block_path = 'pages/test'

    def get(self, ctx):
        form = LoginForm(ctx.req)
        return self._ok({'form': form})
