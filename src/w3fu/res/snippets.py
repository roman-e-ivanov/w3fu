from json import dumps

from w3fu.storage import StorageError


def html(xslt=None):
    def decorator(method):
        def f(res, *args, **kwargs):
            resp = method(res, *args, **kwargs)
            t = None if 'no-xslt' in res.req.query else xslt
            resp.ctype = 'application/xml' if t is None else 'text/html'
            if resp.status == 200:
                resp.content = res.app.xslt.transform(res.name(),
                                                      resp.content,
                                                      t)
            return resp
        return f
    return decorator


def json(method):
    def f(res, *args, **kwargs):
        resp = method(res, *args, **kwargs)
        resp.ctype = 'application/json'
        resp.content = dumps(resp.content)
        return resp
    return f


def storage(method):
    def f(res, *args, **kwargs):
        db = res.app.storage.pull()
        kwargs['db'] = db
        try:
            return method(res, *args, **kwargs)
        except StorageError as e:
            return res.req.response(503, str(e))
        finally:
            res.app.storage.push(db)
    return f


def form(formcls, redirect=True):
    def decorator(method):
        def f(res, *args, **kwargs):
            raw = res.req.content if redirect else res.req.query
            form = formcls(raw)
            if redirect and form.errors:
                return res.req.response(302).location(res.path(res.req.args),
                                                      form.qs())
            kwargs['form'] = form
            return method(res, *args, **kwargs)
        return f
    return decorator


SESSION_NAME = 'u'


def user(method):
    def f(res, db, *args, **kwargs):
        user = None
        try:
            session_id = res.req.cookie[SESSION_NAME].value
            session = db.sessions.find(session_id).fetch()
            if session:
                user = db.users.find(session['user_id']).fetch()
        except KeyError:
            pass
        resp = method(res, db=db, user=user, *args, **kwargs)
        if user is not None and resp.status == 200:
            resp.content['user'] = user
        return resp
    return f
