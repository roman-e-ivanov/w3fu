from datetime import datetime

from w3fu import config
from w3fu.res import bind, Resource
from w3fu.res.middleware.context import storage, user
from w3fu.res.middleware.transform import xml
from w3fu.web import Response
from w3fu.web.forms import Form, StrArg
from w3fu.web.util import Url
from w3fu.storage.orm.auth import User, Session


class AuthForm(Form):

    login = StrArg('login', pattern='^[\w-]+$',
                   min_size=4, max_size=32)
    password = StrArg('password', pattern='^[\x20-\x7e]+$', clear=True,
                      min_size=4, max_size=32)


LoginForm = AuthForm
RegisterForm = AuthForm


@bind('/login')
class Login(Resource):

    @xml('login-html')
    @storage()
    @user()
    def get(self, req):
        form = LoginForm(req.query)
        error = form.src.get('error')
        resp = Response(200, {})
        resp.content['form'] = form.content()
        if error is None:
            return resp
        if error == 'auth':
            resp.content['error'] = {'auth': {}}
        return resp

    @storage()
    def post(self, req):
        form = LoginForm(req.content)
        resp = Response(302)
        if form.err:
            return resp.location(str(Url(req.scheme, req.host, self.path(),
                                         form.src)))
        user = self.db.users.find_by_login(form.data['login']).fetch()
        if user is None or not user.check_password(form.data['password']):
            return resp.location(str(Url(req.scheme, req.host, self.path(),
                                         dict(error='auth', **form.src))))
        session = Session.new(user_id=user['id'])
        self.db.sessions.insert(session)
        self.db.commit()
        resp.set_cookie(config.session_name, session['id'], session['expires'])
        return resp.location(str(Url(req.scheme, req.host, '/home', {})))

    @storage()
    def delete(self, req):
        url = req.referer
        if url is None:
            url = str(Url(req.scheme, req.host))
        resp = Response(302).location(url)
        if config.session_name in req.cookie:
            self.db.sessions.delete(req.cookie[config.session_name].value)
            self.db.commit()
            resp.set_cookie(config.session_name, 0, datetime.utcfromtimestamp(0))
        return resp


@bind('/register')
class Register(Resource):

    @xml('register-html')
    @storage()
    def get(self, req):
        form = RegisterForm(req.query)
        error = form.src.get('error')
        resp = Response(200, {})
        resp.content['form'] = form.content()
        if error is None:
            return resp
        if error == 'exists':
            resp.content['error'] = {'exists': {}}
        return resp

    @storage()
    def post(self, req):
        form = RegisterForm(req.content)
        resp = Response(302)
        if form.err:
            return resp.location(str(Url(req.scheme, req.host, self.path(),
                                         form.src)))
        user = User.new(login=form.data['login'])
        user.password(form.data['password'])
        if not self.db.users.insert(user).count:
            return resp.location(str(Url(req.scheme, req.host, self.path(),
                                         dict(error='exists', **form.src))))
        session = Session.new(user_id=user['id'])
        self.db.sessions.insert(session)
        self.db.commit()
        resp.set_cookie(config.session_name, session['id'], session['expires'])
        return resp.location(str(Url(req.scheme, req.host, '/home', {})))
