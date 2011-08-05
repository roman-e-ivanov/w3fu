from datetime import datetime
from uuid import uuid4

from w3fu import config
from w3fu.storage.documents import Document, Property, Container
from w3fu.data.util import b64e, salted_hash


class Session(Document):

    id = Property('id')
    expires = Property('expires')

    @classmethod
    def new(cls):
        return cls(id=b64e(uuid4().bytes),
                   expires=datetime.utcnow() + config.session_ttl)


class User(Document):

    login = Property('login')
    password = Property('password')
    sessions = Container('sessions', Session)

    @classmethod
    def new(cls, login, password):
        return cls(login=login, password=salted_hash(password))

    def check_password(self, password):
        return self.password == salted_hash(password, self.password)
