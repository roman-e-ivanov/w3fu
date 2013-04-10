from datetime import datetime
from uuid import uuid4

from w3fu.util import b64e, salted_hash
from w3fu.storage import safe, Collection, Document, Property, ID, \
    ListContainer

from app import config


class Session(Document):

    id = Property('id')
    expires = Property('expires')

    def _new(self):
        self.id = b64e(uuid4().bytes)
        self.expires = datetime.utcnow() + config.session_ttl


class User(Document):

    id = ID()
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


class Users(Collection):

    _indexes = [('email', {'unique': True}),
                ('shortcut', {}),
                ('sessions.id', {}),
                ('owned', {})]

    @safe()
    def push_session(self, user, session):
        self._c.update({'_id': user.id},
                       {'$push': {'sessions': session.raw}})

    @safe()
    def pull_session(self, session_id):
        self._c.update({'sessions.id': session_id},
                       {'$pull': {'sessions': {'id': session_id}}})

    @safe()
    def push_owned(self, user, provider_id):
        self._c.update({'_id': user.id},
                       {'$push': {'owned': provider_id}})

    @safe()
    def pull_owned(self, provider_id):
        self._c.update({'owned': provider_id},
                       {'$pull': {'owned': provider_id}})

    @safe()
    def update_password(self, user):
        self._c.update({'_id': user.id},
                       {'$set': {'password': user.password},
                        '$unset': {'shortcut': 1}})

    @safe(True)
    def find_email(self, email):
        return self._c.find_one({'email': email})

    @safe(True)
    def find_shortcut(self, shortcut):
        return self._c.find_one({'shortcut': shortcut})

    @safe(True)
    def find_valid_session(self, session_id, expires):
        query = {'sessions': {'$elemMatch': {'id': session_id,
                                             'expires': {'$gt': expires}}}}
        return self._c.find_one(query)
