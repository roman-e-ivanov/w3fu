from datetime import datetime
from uuid import uuid4

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
    login = Property('login')
    password = Property('password', [])
    sessions = ListContainer('sessions', Session, [])

    def _new(self, login, password):
        self.login = login
        self.password = salted_hash(password)

    def check_password(self, password):
        return self.password == salted_hash(password, self.password)

    def push_session(self, session):
        self.collection.push_session(self.id, session)
        return session
