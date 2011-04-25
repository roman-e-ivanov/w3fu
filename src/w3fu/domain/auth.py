from time import time
from datetime import datetime
from uuid import uuid4

from w3fu import config
from w3fu.domain import Entity
from w3fu.data.util import salted_hash, b64encode


class Session(Entity):

    index = {'index': lambda e: [{'uid': e['uid'], 'expires': e['expires']}]}

    @classmethod
    def _data(cls, user_id):
        return {'user_id': user_id,
                'uid': b64encode(uuid4().bytes),
                'expires': int(time()) + config.session_ttl}

    @classmethod
    def find_valid_uid(cls, db, uid):
        return db.select_index(cls, {'eq': {'uid': uid},
                                     'gt': {'expires': int(time())} },
                                     single=True)

    @property
    def expires(self):
        return datetime.utcfromtimestamp(self['expires'])


class User(Entity):

    index = {'index': lambda e: [{'login': e['login']}]}

    @classmethod
    def _data(cls, login, password):
        return {'login': login, 'password': salted_hash(password)}

    @classmethod
    def login_exists(cls, db, login):
        return db.count_index(cls, {'eq': {'login': login}}) > 0

    @classmethod
    def find_login(cls, db, login):
        return db.select_index(cls, {'eq': {'login': login}}, single=True)

    def check_password(self, value):
        return self['password'] == salted_hash(value, self['password'])
