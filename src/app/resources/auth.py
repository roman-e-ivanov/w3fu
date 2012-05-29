# -*- coding: utf-8 -*-
from w3fu.base import Response
from w3fu.routing import Route
from w3fu.resources import Resource, Form
from w3fu.data.args import StrArg

from app.resources.base import BaseResource
from app.resources.middleware.context import user
from app.resources.middleware.transform import xml
from app.resources.home import Home
from app.resources.index import Index

from app.storage.auth import Users, User, Session


class RegisterForm(Form):

    email = StrArg('email', pattern=u'^[^@]+@[^@]+$',
                   min_size=4, max_size=254)


class SetPasswordForm(Form):

    password = StrArg('password', pattern=u'^[а-яА-Я\x21-\x7e]+$',
                      min_size=4, max_size=32)


class LoginForm(Form):

    email = StrArg('email', pattern=u'^[^@]+@[^@]+$',
                   min_size=4, max_size=254)

    password = StrArg('password', pattern=u'^[а-яА-Я\x21-\x7e]+$',
                      min_size=4, max_size=32)


class Login(Resource):

    route = Route('/login')

    @xml('pages/login/html.xsl')
    @user()
    def get(self, ctx):
        return Response.ok({})

    @xml('pages/login/html.xsl')
    def post(self, ctx):
        form = LoginForm(ctx.req)
        if form.errors:
            return Response.ok({'form': form})
        users = Users(self.ctx.db)
        user = users.find_email(form.data['email'])
        if user is None or not user.check_password(form.data['password']):
            return Response.ok({'form': form, 'user-auth-error': {}})
        session = Session.new()
        users.push_session(user, session)
        ctx.state['session_id'] = session.id
        return Response.redirect(Home.route.url(ctx.req))

    def delete(self, ctx):
        session_id = ctx.state['session_id']
        if session_id is not None:
            users = Users(self.ctx.db)
            users.pull_session(session_id)
        del ctx.state['session_id']
        return Response.redirect(ctx.req.referer or Index.route.url(ctx.req))


class ShortcutLogin(Resource):

    route = Route('/login/{shortcut}',
                  shortcut=StrArg('shortcut', pattern='[\da-zA-Z_-]{22}'))

    @xml('pages/shortcut-login/html.xsl')
    def get(self, ctx):
        users = Users(self.ctx.db)
        user = users.find_shortcut(ctx.args['shortcut'])
        if user is None:
            return Response.not_found()
        return Response.ok({})

    @xml('pages/shortcut-login/html.xsl')
    def post(self, ctx):
        users = Users(self.ctx.db)
        user = users.find_shortcut(ctx.args['shortcut'])
        if user is None:
            return Response.not_found()
        form = SetPasswordForm(ctx.req)
        if form.errors:
            return Response.ok({'form': form})
        user.set_password(form.data['password'])
        users.update_password(user)
        session = Session.new()
        users.push_session(user, session)
        ctx.state['session_id'] = session.id
        return Response.redirect(Home.route.url(ctx.req))


class Register(BaseResource):

    route = Route('/register')

    _block = 'pages/register'

    def post(self, ctx):
        form = RegisterForm(self.rc.req)
        if form.errors:
            return self._bad_request({'form': form})
        users = Users(self.ac.db)
        user = User.new(form.data['email'])
        if not users.insert(user, True):
            return self._conflict({'form': form, 'user_exists': True})
        url = ShortcutLogin.route.url(self.rc.req, shortcut=user.shortcut)
        return self._ok(redirect=url)
