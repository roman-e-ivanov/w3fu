# -*- coding: utf-8 -*-
from datetime import datetime

from w3fu import config
from w3fu.res import bind, Resource
from w3fu.res.middleware.context import user
from w3fu.res.middleware.transform import xml
from w3fu.res.home import Home
from w3fu.res.index import Index
from w3fu.web import Response
from w3fu.web.forms import Form, StrArg
from w3fu.storage.documents.auth import User, Session


class AuthForm(Form):

    login = StrArg('login', pattern=u'^[\wа-яА-Я\._-]+$',
                   min_size=4, max_size=32)
    password = StrArg('password', pattern=u'^[а-яА-Я\x21-\x7e]+$', clear=True,
                      min_size=4, max_size=32)


LoginForm = AuthForm
RegisterForm = AuthForm


@bind('/login')
class Login(Resource):

    @xml('login-html')
    @user(dump='xml')
    def get(self, app, req):
        resp = Response(200, {'form': LoginForm(req.fs).dump()})
        if req.fs.getfirst('error') == 'auth':
            resp.content['error'] = {'auth': {}}
        return resp

    def post(self, app, req):
        form = LoginForm(req.fs)
        resp = Response(302)
        if form.err:
            return resp.location(self.url(form.src))
        user = User.find_login(app.storage, form.data['login'])
        if user is None or not user.check_password(form.data['password']):
            return resp.location(self.url(dict(error='auth', **form.src)))
        session = Session.new()
        user.push_session(session)
        resp.set_cookie(config.session_name, session.id, session.expires)
        return resp.location(Home.url())

    def delete(self, app, req):
        resp = Response(302).location(req.referer or Index.url())
        sid = req.cookie.get(config.session_name)
        if sid is not None:
            User.pull_session(app.storage, sid.value)
        resp.set_cookie(config.session_name, 0, datetime.utcfromtimestamp(0))
        return resp


@bind('/register')
class Register(Resource):

    @xml('register-html')
    def get(self, app, req):
        resp = Response(200, {'form': RegisterForm(req.fs).dump()})
        if req.fs.getfirst('error') == 'exists':
            resp.content['error'] = {'exists': {}}
        return resp

    def post(self, app, req):
        form = RegisterForm(req.fs)
        resp = Response(302)
        if form.err:
            return resp.location(self.url(form.src))
        user = User.new(form.data['login'], form.data['password'])
        session = Session.new()
        user.sessions = [session]
        if not User.insert(app.storage, user):
            return resp.location(self.url(dict(error='exists', **form.src)))
        resp.set_cookie(config.session_name, session.id, session.expires)
        return resp.location(Home.url())
