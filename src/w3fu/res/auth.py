import sys
from openid.consumer.consumer import Consumer, DiscoveryFailure, SUCCESS
from pprint import pprint

from w3fu import config
from w3fu.res import bind, Resource
from w3fu.res.snippets import html, storage, user
from w3fu.data.forms import Form, Arg
from w3fu.storage.orm.auth import User, Session


SESSION_NAME = 'u'
SESSION_TTL = 24 * 3600


class AuthForm(Form):

    login = Arg()
    password = Arg()


LoginForm = AuthForm
RegisterForm = AuthForm


@bind('/login')
class Login(Resource):

    @html('login-html')
    @storage
    @user
    def get(self, db, user):
        form = LoginForm(self.req.query)
        error = form.raw.get('error')
        resp = self.req.response(200, {})
        resp.content['form'] = form.content()
        if error is None:
            return resp
        if error == 'auth':
            resp.content['error'] = {'auth': {}}
        return resp

    @html()
    @storage
    def post(self, db):
        form = LoginForm(self.req.content)
        resp = self.req.response(302)
        if form.errors:
            return resp.location(self.path(), form.raw)
        user = db.users.find_by_login(form.values['login']).fetch()
        if user is None or not user.check_password(form.values['password']):
            return resp.location(self.path(), dict(error='auth', **form.raw))
        session = Session(user_id=user['id'])
        db.sessions.insert(session, SESSION_TTL)
        db.commit()
        resp.set_cookie(config.session_name, session['id'], config.session_ttl)
        return resp.location('/home')


@bind('/register')
class Register(Resource):

    @html('register-html')
    @storage
    def get(self, db, form):
        form = RegisterForm(self.req.query)
        error = form.raw.get('error')
        resp = self.req.response(200, {})
        resp.content['form'] = form.content()
        if error is None:
            return resp
        if error == 'exists':
            resp.content['error'] = {'exists': {}}
        return resp

    @html()
    @storage
    def post(self, db, form):
        form = RegisterForm(self.req.content)
        resp = self.req.response(302)
        if form.errors:
            return resp.location(self.path(), form.raw)
        user = User(**form.values)
        if not db.users.insert(user).count:
            return resp.location(self.path(), dict(error='exists', **form.raw))
        session = Session(user_id=user['id'])
        db.sessions.insert(session, SESSION_TTL)
        db.commit()
        resp.set_cookie(config.session_name, session['id'], config.session_ttl)
        return resp.location('/home')


class OpenIdAuth(Resource):

    def get(self):
        consumer = Consumer(self.app.session, self.app.store)
        try:
            authrequest = consumer.begin('openid.yandex.ru/roman.e.ivanov')
            #authrequest = consumer.begin('https://www.google.com/accounts/o8/id')
        except DiscoveryFailure:
            return self.req.response(401, content='Unauthorized')
        rurl = authrequest.redirectURL('http://localhost',
                                       return_to='http://localhost/profile',
                                       immediate=False);
        return self.req.response(302).location(rurl)


class OpenIdProfile(Resource):

    def get(self):
        pprint(self.req.qargs, sys.stderr)
        consumer = Consumer(self.app.session, self.app.store)
        info = consumer.complete(self.req.qargs, 'http://localhost/profile')
        self.app.session = {}
        if info.status == SUCCESS:
            return self.req.response(200, content="OK")
        return self.req.response(401, 'Unauthorized')
