from uuid import uuid4
from datetime import datetime

from w3fu import config
from w3fu.data.domain import Row
from w3fu.data.util import salted_hash, b64encode


class User(Row):

    def check_password(self, value):
        return self['password'] == salted_hash(value, self['password'])

    def password(self, value):
        self['password'] = salted_hash(value)


class Session(Row):

    def _new(self):
        self['id'] = b64encode(uuid4().bytes)
        self['expires'] = datetime.utcnow() + config.session_ttl
