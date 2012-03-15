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
    email = Property('email')
    password = Property('password', [])
    shortcut = Property('shortcut')
    sessions = ListContainer('sessions', Session, [])

    def _new(self, email):
        self.email = email
        self.shortcut = b64e(uuid4().bytes)

    def set_password(self, password):
        self.password = salted_hash(password)
        del self.shortcut

    def check_password(self, password):
        return self.password == salted_hash(password, self.password)
