from uuid import uuid4
from time import time
from datetime import datetime

from w3fu import config
from w3fu.domain import Entity
from w3fu.data.util import salted_hash, b64encode


class Session(Entity):

    index = {
             'index': lambda e: [{
                                  'uuid': e['uuid'],
                                  'expires': e['expires']
                                  }]
             }

    @classmethod
    def _data(cls):
        return {
                'uuid': b64encode(uuid4().bytes),
                'expires': int(time()) + config.session_ttl
                }

    @property
    def expires(self):
        return datetime.utcfromtimestamp(self['expires'])

    @classmethod
    def find_valid(cls, db, uuid):
        sessions = db.select_index(cls, {
                                         'eq': {'uuid': uuid},
                                         'gt': {'expires': int(time())},
                                         })
        return sessions[0] if sessions else None

    @classmethod
    def delete_uuid(cls, db, uuid):
        pass


class User(Entity):

    index = {
             'index': lambda e: [{'login': e['login']}]
             }

    @classmethod
    def find_by_login(cls, db, login):
        users = db.select_index(cls, {'eq': {'login': login}})
        return users[0] if users else None

    @classmethod
    def login_exists(cls, db, login):
        return db.count_index(cls, {'eq': {'login': login}}) > 0

    def set_password(self, value):
        self['password'] = salted_hash(value)

    def check_password(self, value):
        return self['password'] == salted_hash(value, self['password'])
