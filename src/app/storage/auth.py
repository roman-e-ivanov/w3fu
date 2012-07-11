from datetime import datetime
from uuid import uuid4

from w3fu.util import b64e, salted_hash
from w3fu.storage import safe, Property, ListContainer

from app import config
from app.storage import Model


class Session(Model):

    id = Property('id')
    expires = Property('expires')

    def _new(self):
        self.id = b64e(uuid4().bytes)
        self.expires = datetime.utcnow() + config.session_ttl


class User(Model):

    _collection = 'users'
    _indexes = [('email', {'unique': True}),
                ('shortcut', {}),
                ('sessions.id', {}),
                ('owned', {})]

    id = Property('_id')
    email = Property('email')
    password = Property('password', hidden=True)
    shortcut = Property('shortcut')
    owned = Property('owned', hidden=True)
    sessions = ListContainer('sessions', Session, hidden=True)

    def _new(self, email):
        self.email = email
        self.shortcut = b64e(uuid4().bytes)

    def set_password(self, password):
        self.password = salted_hash(password)
        del self.shortcut

    def check_password(self, password):
        return self.password == salted_hash(password, self.password)

    def can_write(self, provider_id):
        return provider_id in self.owned

    @classmethod
    @safe()
    def push_session(cls, user, session):
        cls._c().update({'_id': user.id},
                      {'$push': {'sessions': session.raw}})

    @classmethod
    @safe()
    def pull_session(cls, session_id):
        cls._c().update({'sessions.id': session_id},
                      {'$pull': {'sessions': {'id': session_id}}})

    @classmethod
    @safe()
    def push_owned(cls, user, provider_id):
        cls._c().update({'_id': user.id},
                       {'$push': {'owned': provider_id}})

    @classmethod
    @safe()
    def pull_owned(cls, provider_id):
        cls._c().update({'owned': provider_id},
                      {'$pull': {'owned': provider_id}})

    @classmethod
    @safe()
    def update_password(cls, user):
        cls._c().update({'_id': user.id},
                      {'$set': {'password': user.password},
                       '$unset': {'shortcut': 1}})

    @classmethod
    @safe(True)
    def find_email(cls, email):
        return cls._c().find_one({'email': email})

    @classmethod
    @safe(True)
    def find_shortcut(cls, shortcut):
        return cls._c().find_one({'shortcut': shortcut})

    @classmethod
    @safe(True)
    def find_valid_session(cls, id, expires):
        query = {'sessions': {'$elemMatch': {'id': id,
                                             'expires': {'$gt': expires}}}}
        return cls._c().find_one(query)
