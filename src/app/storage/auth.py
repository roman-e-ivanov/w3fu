from datetime import datetime
from uuid import uuid4

from w3fu import storage
from w3fu.data.codecs import b64e, salted_hash

from app import config


class Session(storage.Model):

    id = storage.Property('id')
    expires = storage.Property('expires')

    def _new(self):
        self.id = b64e(uuid4().bytes)
        self.expires = datetime.utcnow() + config.session_ttl


class User(storage.Model):

    _collection = 'users'
    _indexes = [('email', {'unique': True}),
                ('shortcut', {}),
                ('sessions.id', {}),
                ('owned', {})]

    id = storage.Property('_id')
    email = storage.Property('email')
    password = storage.Property('password', hidden=True)
    shortcut = storage.Property('shortcut')
    owned = storage.Property('owned', hidden=True)
    sessions = storage.ListContainer('sessions', Session, hidden=True)

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
    @storage.safe()
    def push_session(cls, user, session):
        cls._c().update({'_id': user.id},
                      {'$push': {'sessions': session.raw}})

    @classmethod
    @storage.safe()
    def pull_session(cls, session_id):
        cls._c().update({'sessions.id': session_id},
                      {'$pull': {'sessions': {'id': session_id}}})

    @classmethod
    @storage.safe()
    def push_owned(cls, user, provider_id):
        cls._c().update({'_id': user.id},
                       {'$push': {'owned': provider_id}})

    @classmethod
    @storage.safe()
    def pull_owned(cls, provider_id):
        cls._c().update({'owned': provider_id},
                      {'$pull': {'owned': provider_id}})

    @classmethod
    @storage.safe()
    def update_password(cls, user):
        cls._c().update({'_id': user.id},
                      {'$set': {'password': user.password},
                       '$unset': {'shortcut': 1}})

    @classmethod
    @storage.safe(True)
    def find_email(cls, email):
        return cls._c().find_one({'email': email})

    @classmethod
    @storage.safe(True)
    def find_shortcut(cls, shortcut):
        return cls._c().find_one({'shortcut': shortcut})

    @classmethod
    @storage.safe(True)
    def find_valid_session(cls, id, expires):
        query = {'sessions': {'$elemMatch': {'id': id,
                                             'expires': {'$gt': expires}}}}
        return cls._c().find_one(query)
