# -*- coding: utf-8 -*-
from w3fu import args, http, routing, resources

from app.resources import base
from app.resources.middleware.context import user
from app.resources.middleware.transform import xml
from app.resources.home import Home
from app.resources.index import Index

from app.storage import auth


class RegisterForm(resources.Form):

    email = args.StrArg('email', pattern=u'^[^@]+@[^@]+$',
                        min_size=4, max_size=254)


class SetPasswordForm(resources.Form):

    password = args.StrArg('password', pattern=u'^[а-яА-Я\x21-\x7e]+$',
                           min_size=4, max_size=32)


class LoginForm(resources.Form):

    email = args.StrArg('email', pattern=u'^[^@]+@[^@]+$',
                        min_size=4, max_size=254)

    password = args.StrArg('password', pattern=u'^[а-яА-Я\x21-\x7e]+$',
                           min_size=4, max_size=32)


class Login(resources.Resource):

    route = routing.Route('/login')

    @xml('pages/login/html.xsl')
    @user()
    def get(self, ctx):
        return http.Response.ok({})

    @xml('pages/login/html.xsl')
    def post(self, ctx):
        form = LoginForm(ctx.req)
        if form.errors:
            return http.Response.ok({'form': form})
        user = auth.User.find_email(form.data['email'])
        if user is None or not user.check_password(form.data['password']):
            return http.Response.ok({'form': form, 'user-auth-error': {}})
        session = auth.Session.new()
        auth.User.push_session(user, session)
        ctx.state['session_id'] = session.id
        return http.Response.redirect(Home.route.url(ctx.req))

    def delete(self, ctx):
        session_id = ctx.state['session_id']
        if session_id is not None:
            auth.User.pull_session(session_id)
        del ctx.state['session_id']
        return http.Response.redirect(ctx.req.referer or Index.route.url(ctx.req))


class ShortcutLogin(resources.Resource):

    route = routing.Route('/login/{shortcut}',
                          shortcut=args.StrArg('shortcut',
                                               pattern='[\da-zA-Z_-]{22}'))

    @xml('pages/shortcut-login/html.xsl')
    def get(self, ctx):
        user = auth.User.find_shortcut(ctx.args['shortcut'])
        if user is None:
            return http.Response.not_found()
        return http.Response.ok({})

    @xml('pages/shortcut-login/html.xsl')
    def post(self, ctx):
        user = auth.User.find_shortcut(ctx.args['shortcut'])
        if user is None:
            return http.Response.not_found()
        form = SetPasswordForm(ctx.req)
        if form.errors:
            return http.Response.ok({'form': form})
        user.set_password(form.data['password'])
        auth.User.update_password(user)
        session = auth.Session.new()
        auth.User.push_session(user, session)
        ctx.state['session_id'] = session.id
        return http.Response.redirect(Home.route.url(ctx.req))


class Register(base.BaseResource):

    route = routing.Route('/register')

    _block_path = 'pages/register'

    def post(self, ctx):
        form = RegisterForm(self.rc.req)
        if form.errors:
            return self._bad_request({'form': form})
        user = auth.User.new(form.data['email'])
        if not auth.User.insert(user, True):
            return self._conflict({'form': form, 'user_exists': True})
        url = ShortcutLogin.route.url(self.rc.req, shortcut=user.shortcut)
        return self._ok(redirect=url)
