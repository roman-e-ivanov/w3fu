from uuid import uuid4
from datetime import datetime

from w3fu import config
from w3fu.storage.data import Entity, Column
from w3fu.data.util import salted_hash, b64encode


class User(Entity):

    id = Column(pk=True, auto=True)
    login = Column()
    password = Column()

    @classmethod
    def find_by_login(cls, db, login):
        q = db.query()
        found = db.select(cls, q(cls.login) == login)
        return found[0] if found else None

    @password.setter
    def set_password(self, value):
        return salted_hash(value)

    def check_password(self, value):
        return self.password == salted_hash(value, self.password)


class Session(Entity):

    id = Column(pk=True, auto=False)
    user_id = Column()
    expires = Column()

    def _new(self):
        self.id = b64encode(uuid4().bytes)
        self.expires = datetime.utcnow() + config.session_ttl

    @classmethod
    def find(cls, db, id):
        q = db.query()
        found = db.select(cls, (q(cls.pk) == id) &
                          (q(cls.expires) > datetime.utcnow()))
        return found[0] if found else None
