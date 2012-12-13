# -*- coding: utf-8 -*-
from w3fu.http import OK, Redirect, BadRequest, NotFound, Conflict
from w3fu.resources import Resource, Form, HTML
from w3fu.args import StrArg

from app.routing import router
from app.view import view
from app.storage.auth import User
from app.state import UserState
from app.mixins import public_mixins


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

    html = HTML(view['pages/login'], public_mixins)

    @html.GET
    def get(self, req):
        return OK({})

    @html.POST
    @LoginForm.handler()
    def post(self, req):
        user = User.find_email(req.form.data['email'])
        if user is None or not user.check_password(req.form.data['password']):
            raise BadRequest({'error': 'user-auth'})
        resp = Redirect(router['home'].url(req))
        UserState.login(resp, user)
        raise resp

    @html.DELETE
    def delete(self, req):
        resp = Redirect(req.referer or router['index'].url(req))
        UserState.logout(req, resp)
        raise resp


class ShortcutLogin(Resource):

    html = HTML(view['pages/shortcut-login'], public_mixins)

    def __call__(self, req, shortcut):
        user = User.find_shortcut(shortcut)
        if user is None:
            raise NotFound
        return super(ShortcutLogin, self).__call__(req, user=user)

    @html.GET
    def get(self, req, user):
        return OK({})

    @html.POST
    @SetPasswordForm.handler()
    def post(self, req, user):
        user.set_password(req.form.data['password'])
        User.update_password(user)
        resp = Redirect(router['home'].url(req))
        UserState.login(resp, user)
        raise resp


class Register(Resource):

    html = HTML(view['pages/register'], public_mixins)

    @html.GET
    def get(self, req):
        return OK({})

    @html.POST
    @RegisterForm.handler()
    def post(self, req):
        user = User.new(req.form.data['email'])
        if not User.insert(user, True):
            raise Conflict({'error': 'user-exists'})
        raise Redirect(router['shortcut_login'].url(req,
                                                    shortcut=user.shortcut))
