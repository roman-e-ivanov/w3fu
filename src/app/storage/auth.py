from datetime import datetime
from uuid import uuid4

from w3fu.storage.collections import Collection, errorsafe, wrapped
from w3fu.storage.documents import Document, Property, ListContainer
from w3fu.data.codecs import b64e, salted_hash

from app import config


class Session(Document):

    id = Property('id')
    expires = Property('expires')

    def _new(self):
        self.id = b64e(uuid4().bytes)
        self.expires = datetime.utcnow() + config.session_ttl


class User(Document):

    id = Property('_id')
    email = Property('email')
    password = Property('password', formats=[])
    shortcut = Property('shortcut')
    owned = Property('owned', default=[])
    sessions = ListContainer('sessions', Session, formats=[])

    def _new(self, email):
        self.email = email
        self.shortcut = b64e(uuid4().bytes)

    def set_password(self, password):
        self.password = salted_hash(password)
        del self.shortcut

    def check_password(self, password):
        return self.password == salted_hash(password, self.password)

    def can_write(self, provider_id):
        return provider_id in self.own


class Users(Collection):

    _doc_cls = User
    _indexes = [('email', {'unique': True}),
                ('shortcut', {}),
                ('sessions.id', {}),
                ('owned', {})]

    @errorsafe
    def push_session(self, user, session):
        self._collection.update({'_id': user.id},
                                {'$push': {'sessions': session.raw}})

    @errorsafe
    def pull_session(self, session_id):
        self._collection.update({'sessions.id': session_id},
                                {'$pull': {'sessions': {'id': session_id}}})

    @errorsafe
    def push_owned(self, user, provider_id):
        self._collection.update({'_id': user.id},
                                {'$push': {'owned': provider_id}})

    @errorsafe
    def pull_owned(self, provider_id):
        self._collection.update({'owned': provider_id},
                                {'$pull': {'owned': provider_id}})

    @errorsafe
    def update_password(self, user):
        self._collection.update({'_id': user.id},
                                {'$set': {'password': user.password},
                                 '$unset': {'shortcut': 1}})

    @wrapped
    @errorsafe
    def find_email(self, email):
        return self._collection.find_one({'email': email})

    @wrapped
    @errorsafe
    def find_shortcut(self, shortcut):
        return self._collection.find_one({'shortcut': shortcut})

    @wrapped
    @errorsafe
    def find_valid_session(self, id, expires):
        query = {'sessions': {'$elemMatch': {'id': id,
                                             'expires': {'$gt': expires}}}}
        return self._collection.find_one(query)
