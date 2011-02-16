from w3fu import config
from w3fu.res import bind, Resource
from w3fu.res.snippets import html, storage, user
from w3fu.web.forms import Form, StrArg
from w3fu.web.util import Url
from w3fu.storage.orm.auth import User, Session


SESSION_NAME = 'u'
SESSION_TTL = 24 * 3600


class AuthForm(Form):

    login = StrArg('login', pattern='^[\w-]+$',
                   min_size=4, max_size=32)
    password = StrArg('password', pattern='^[\x20-\x7e]+$', clear=True,
                      min_size=4, max_size=32)


LoginForm = AuthForm
RegisterForm = AuthForm


@bind('/login')
class Login(Resource):

    @html('login-html')
    @storage
    @user
    def get(self, db, user):
        form = LoginForm(self.req.query)
        error = form.src.get('error')
        resp = self.req.response(200, {})
        resp.content['form'] = form.content()
        if error is None:
            return resp
        if error == 'auth':
            resp.content['error'] = {'auth': {}}
        return resp

    @storage
    def post(self, db):
        form = LoginForm(self.req.content)
        resp = self.req.response(302)
        if form.err:
            return resp.location(str(Url(self.req.scheme, self.req.host,
                                         self.path(), form.src)))
        user = db.users.find_by_login(form.data['login']).fetch()
        if user is None or not user.check_password(form.data['password']):
            return resp.location(str(Url(self.req.scheme, self.req.host,
                                         self.path(),
                                         dict(error='auth', **form.src))))
        session = Session(user_id=user['id'])
        db.sessions.insert(session, SESSION_TTL)
        db.commit()
        resp.set_cookie(config.session_name, session['id'], config.session_ttl)
        return resp.location(str(Url(self.req.scheme,
                                     self.req.host, '/home', {})))

    @storage
    def delete(self, db):
        url = self.req.referer
        if url is None:
            url = str(Url(self.req.scheme, self.req.host))
        resp = self.req.response(302).location(url)
        if config.session_name in self.req.cookie:
            db.sessions.delete(self.req.cookie[config.session_name].value)
            db.commit()
            resp.set_cookie(config.session_name, 0, -1000000)
        return resp


@bind('/register')
class Register(Resource):

    @html('register-html')
    @storage
    def get(self, db, form):
        form = RegisterForm(self.req.query)
        error = form.src.get('error')
        resp = self.req.response(200, {})
        resp.content['form'] = form.content()
        if error is None:
            return resp
        if error == 'exists':
            resp.content['error'] = {'exists': {}}
        return resp

    @storage
    def post(self, db, form):
        form = RegisterForm(self.req.content)
        resp = self.req.response(302)
        if form.err:
            return resp.location(str(Url(self.req.scheme, self.req.host,
                                         self.path(), form.src)))
        user = User(**form.data)
        if not db.users.insert(user).count:
            return resp.location(str(Url(self.req.scheme, self.req.host,
                                         self.path(),
                                         dict(error='exists', **form.src))))
        session = Session(user_id=user['id'])
        db.sessions.insert(session, SESSION_TTL)
        db.commit()
        resp.set_cookie(config.session_name, session['id'], config.session_ttl)
        return resp.location(str(Url(self.req.scheme,
                                     self.req.host, '/home', {})))
