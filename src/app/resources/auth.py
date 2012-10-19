# -*- coding: utf-8 -*-
from w3fu.http import OK, Redirect, BadRequest, NotFound, Conflict
from w3fu.routing import Route
from w3fu.resources import Resource, Form, HTML
from w3fu.args import StrArg

from app.view import blocks
from app.resources.home import Home
from app.resources.index import Index
from app.storage.auth import User, Session


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

    html = HTML(blocks['pages/login'])

    @html.GET
    def get(self, ctx):
        return OK({})

    @html.POST
    def post(self, ctx):
        form = LoginForm(ctx.req)
        if form.errors:
            return BadRequest({'form': form})
        user = User.find_email(form.data['email'])
        if user is None or not user.check_password(form.data['password']):
            raise BadRequest({'form': form, 'user-auth-error': {}})
        session = Session.new()
        User.push_session(user, session)
        ctx.state['session_id'] = session.id
        raise Redirect(Home.route.url(ctx.req))

    @html.DELETE
    def delete(self, ctx):
        session_id = ctx.state['session_id']
        if session_id is not None:
            User.pull_session(session_id)
        del ctx.state['session_id']
        raise Redirect(ctx.req.referer or Index.route.url(ctx.req))


class ShortcutLogin(Resource):

    route = Route('/login/{shortcut}',
                  shortcut=StrArg('shortcut', pattern='[\da-zA-Z_-]{22}'))

    html = HTML(blocks['pages/shortcut-login'])

    def __call__(self, ctx, shortcut):
        user = User.find_shortcut(shortcut)
        if user is None:
            raise NotFound
        super(ShortcutLogin, self).__call__(ctx, user=user)

    @html.GET
    def get(self, ctx, user):
        return OK({})

    @html.POST
    def post(self, ctx, user):
        form = SetPasswordForm(ctx.req)
        if form.errors:
            raise BadRequest({'form': form})
        user.set_password(form.data['password'])
        User.update_password(user)
        session = Session.new()
        User.push_session(user, session)
        ctx.state['session_id'] = session.id
        raise Redirect(Home.route.url(ctx.req))


class Register(Resource):

    route = Route('/register')

    html = HTML(blocks['pages/register'])

    @html.GET
    def get(self, ctx):
        return OK({})

    @html.POST
    def post(self, ctx):
        form = RegisterForm(ctx.req)
        if form.errors:
            raise BadRequest({'form': form})
        user = User.new(form.data['email'])
        if not User.insert(user, True):
            raise Conflict({'form': form, 'user_exists': True})
        raise Redirect(ShortcutLogin.route.url(ctx.req, shortcut=user.shortcut))
