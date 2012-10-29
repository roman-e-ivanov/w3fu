# -*- coding: utf-8 -*-
from w3fu.http import OK, Redirect, BadRequest, NotFound, Conflict
from w3fu.routing import Route
from w3fu.resources import Resource, Form, HTML
from w3fu.args import StrArg

from app.view import blocks
from app.resources.home import Home
from app.resources.index import Index
from app.storage.auth import User, Session
from app.state import SessionIdState

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
    def get(self, req):
        return OK({})

    @html.POST
    def post(self, req):
        form = LoginForm(req)
        if form.errors:
            return BadRequest({})
        user = User.find_email(form.data['email'])
        if user is None or not user.check_password(form.data['password']):
            raise BadRequest({'user_auth_error': True})
        session = Session.new()
        User.push_session(user, session)
        resp = Redirect(Home.route.url(req))
        SessionIdState.set(resp, session.id)
        raise resp

    @html.DELETE
    def delete(self, req):
        if req.session_id is not None:
            User.pull_session(req.session_id)
        resp = Redirect(req.referer or Index.route.url(req))
        SessionIdState.delete(resp)
        raise resp


class ShortcutLogin(Resource):

    route = Route('/login/{shortcut}',
                  shortcut=StrArg('shortcut', pattern='[\da-zA-Z_-]{22}'))

    html = HTML(blocks['pages/shortcut-login'])

    def __call__(self, req, shortcut):
        user = User.find_shortcut(shortcut)
        if user is None:
            raise NotFound
        super(ShortcutLogin, self).__call__(req, user=user)

    @html.GET
    def get(self, req, user):
        return OK({})

    @html.POST
    def post(self, req, user):
        form = SetPasswordForm(req)
        if form.errors:
            raise BadRequest({})
        user.set_password(form.data['password'])
        User.update_password(user)
        session = Session.new()
        User.push_session(user, session)
        resp = Redirect(Home.route.url(req))
        SessionIdState.set(resp, session.id)
        raise resp


class Register(Resource):

    route = Route('/register')

    html = HTML(blocks['pages/register'])

    @html.GET
    def get(self, req):
        return OK({})

    @html.POST
    def post(self, req):
        form = RegisterForm(req)
        if form.errors:
            raise BadRequest({})
        user = User.new(form.data['email'])
        if not User.insert(user, True):
            raise Conflict({'user_exists': True})
        raise Redirect(ShortcutLogin.route.url(req, shortcut=user.shortcut))
