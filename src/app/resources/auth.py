# -*- coding: utf-8 -*-
from datetime import datetime

from w3fu.base import Response
from w3fu.routing import Route
from w3fu.resources import Resource, Form
from w3fu.data.args import StrArg

from app import config
from app.cookies import AuthCookie

from app.resources.middleware.context import user
from app.resources.middleware.transform import xml
from app.resources.home import Home
from app.resources.index import Index

from app.storage.collections.auth import Users
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
    def get(self, req):
        return Response.ok({'form': LoginForm(req)})

    def post(self, req):
        form = LoginForm(req, True)
        if form.errors:
            return Response.redirect(self.route.url(req, form.query()))
        users = Users(self.ctx.db)
        user = users.find_login(form.data['login'])
        if user is None or not user.check_password(form.data['password']):
            query = form.query(error='auth')
            return Response.redirect(self.route.url(req, query))
        session = Session.new()
        user.push_session(session)
        resp = Response.redirect(Home.route.url(req))
        AuthCookie(req).set(resp, 'session_id', session.id)
        return resp

    def delete(self, req):
        session_id = req.cookie.get(config.session_cookie)
        if session_id is not None:
            print(session_id)
            users = Users(self.ctx.db)
            users.pull_session(session_id)
        resp = Response.redirect(req.referer or Index.route.url(req))
        AuthCookie(req).remove(resp, 'session_id')
        return resp


class Register(Resource):

    route = Route('/register')

    @xml('register-html.xsl')
    def get(self, req):
        return Response.ok({'form': RegisterForm(req)})

    def post(self, req):
        form = RegisterForm(req, True)
        if form.errors:
            return Response.redirect(self.route.url(req, form.query()))
        users = Users(self.ctx.db)
        user = User.new(form.data['login'], form.data['password'])
        session = Session.new()
        user.sessions = [session]
        if not users.insert(user):
            query = form.query(error='exists')
            return Response.redirect(self.route.url(req, query))
        resp = Response.redirect(Home.route.url(req))
        AuthCookie(req).set(resp, 'session_id', session.id)
        return resp
