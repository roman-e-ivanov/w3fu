# -*- coding: utf-8 -*-
from w3fu.base import Response
from w3fu.routing import Route
from w3fu.resources import Resource, Form
from w3fu.data.args import StrArg

from app.resources.middleware.context import user
from app.resources.middleware.transform import xml
from app.resources.home import Home
from app.resources.index import Index

from app.storage.collections.auth import Users
from app.storage.documents.auth import User, Session


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

    @xml('login-html.xsl')
    @user()
    def get(self, req):
        return Response.ok({})

    @xml('login-html.xsl')
    def post(self, req):
        form = LoginForm(req)
        if form.errors:
            return Response.ok({'form': form})
        users = Users(self.ctx.db)
        user = users.find_email(form.data['email'])
        if user is None or not user.check_password(form.data['password']):
            return Response.ok({'form': form, 'user-auth-error': {}})
        session = Session.new()
        users.push_session(user, session)
        req.ctx.state['session_id'] = session.id
        return Response.redirect(Home.route.url(req))

    def delete(self, req):
        session_id = req.ctx.state['session_id']
        if session_id is not None:
            users = Users(self.ctx.db)
            users.pull_session(session_id)
        del req.ctx.state['session_id']
        return Response.redirect(req.referer or Index.route.url(req))


class ShortcutLogin(Resource):

    route = Route('/login/{shortcut}',
                  shortcut=StrArg('shortcut', pattern='[\da-zA-Z_-]{22}'))

    @xml('shortcut-login-html.xsl')
    def get(self, req):
        users = Users(self.ctx.db)
        user = users.find_shortcut(req.ctx.args['shortcut'])
        if user is None:
            return Response.not_found()
        return Response.ok({})

    @xml('shortcut-login-html.xsl')
    def post(self, req):
        users = Users(self.ctx.db)
        user = users.find_shortcut(req.ctx.args['shortcut'])
        if user is None:
            return Response.not_found()
        form = SetPasswordForm(req)
        if form.errors:
            return Response.ok({'form': form})
        user.set_password(form.data['password'])
        users.update_password(user)
        session = Session.new()
        users.push_session(user, session)
        req.ctx.state['session_id'] = session.id
        return Response.redirect(Home.route.url(req))


class Register(Resource):

    route = Route('/register')

    @xml('register-html.xsl')
    def get(self, req):
        return Response.ok({})

    @xml('register-html.xsl')
    def post(self, req):
        form = RegisterForm(req)
        if form.errors:
            return Response.ok({'form': form})
        users = Users(self.ctx.db)
        user = User.new(form.data['email'])
        if not users.insert(user):
            return Response.ok({'form': form, 'user-exists-error': {}})
        url = ShortcutLogin.route.url(req, shortcut=user.shortcut)
        return Response.redirect(url)
