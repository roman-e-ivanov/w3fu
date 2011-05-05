from datetime import datetime
from uuid import uuid4

from w3fu import config
from w3fu.domain import Entity, r, w
from w3fu.data.util import b64e, salted_hash


class Session(Entity):

    delete_uid = w('delete from {self} where uid=%(uid)s')

    find_valid_uid = r('''
        select * from {self} where uid=%(uid)s and expires>%(time)s
    ''', True)

    @classmethod
    def new(cls, user):
        return cls(user_id=user['id'],
                   user_name=user.visible_name(),
                   uid=b64e(uuid4().bytes),
                   expires=datetime.utcnow() + config.session_ttl)


class User(Entity):

    find_login = r('select * from {self} where login=%(login)s', True)

    @classmethod
    def new(cls, login, password):
        return cls(login=login,
                   password=salted_hash(password))

    def check_password(self, value):
        return self['password'] == salted_hash(value, self['password'])

    def visible_name(self):
        return self['login']
