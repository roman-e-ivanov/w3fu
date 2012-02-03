# -*- coding: utf-8 -*-
from datetime import datetime

from w3fu.web.resources import Route, Resource
from w3fu.web.base import Response
from w3fu.web.forms import Form, StrArg

from app import config
from app.resources.middleware.context import user
from app.resources.middleware.transform import xml
from app.resources.home import Home
from app.resources.index import Index
from app.storage.documents.auth import User, Session


class AuthForm(Form):

    login = StrArg('login', pattern=u'^[\wа-яА-Я\._-]+$',
                   min_size=4, max_size=32)
    password = StrArg('password', pattern=u'^[а-яА-Я\x21-\x7e]+$', clear=True,
                      min_size=4, max_size=32)
    error = StrArg('error', default='')


LoginForm = AuthForm
RegisterForm = AuthForm


class Login(Resource):

    route = Route('/login')

    @xml('login-html.xsl')
    @user()
    def get(self, app, req):
        return Response(200, {'form': LoginForm(req.fs)})

    def post(self, app, req):
        form = LoginForm(req.fs, True)
        resp = Response(302)
        if form.err:
            return resp.location(self.route.url(req, form.query()))
        user = app.storage.users.find_login(form.data['login'])
        if user is None or not user.check_password(form.data['password']):
            form.data['error'] = 'auth'
            return resp.location(self.route.url(req, form.query()))
        session = Session.new(app.storage.users)
        user.push_session(session)
        resp.set_cookie(config.session_cookie, session.id, session.expires)
        return resp.location(Home.route.url(req))

    def delete(self, app, req):
        resp = Response(302).location(req.referer or Index.route.url(req))
        session_id = req.cookie.get(config.session_cookie)
        if session_id is not None:
            app.storage.users.pull_session(session_id.value)
        resp.set_cookie(config.session_cookie, 0, datetime.utcfromtimestamp(0))
        return resp


class Register(Resource):

    route = Route('/register')

    @xml('register-html.xsl')
    def get(self, app, req):
        return Response(200, {'form': RegisterForm(req.fs)})

    def post(self, app, req):
        form = RegisterForm(req.fs, True)
        resp = Response(302)
        if form.err:
            return resp.location(self.route.url(req, form.query()))
        user = User.new(app.storage.users, form.data['login'], form.data['password'])
        session = Session.new(app.storage.users)
        user.sessions = [session]
        if not user.insert():
            form.data['error'] = 'exists'
            return resp.location(self.route.url(req, form.query()))
        resp.set_cookie(config.session_cookie, session.id, session.expires)
        return resp.location(Home.route.url(req))
