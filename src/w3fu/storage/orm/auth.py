from uuid import uuid4
from datetime import datetime

from w3fu import config
from w3fu.storage.orm import Mapper, Row
from w3fu.data.util import salted_hash, b64encode


class User(Row):

    fields = frozenset(('login', 'password'))

    def check_password(self, value):
        return self['password'] == salted_hash(value, self['password'])

    @property
    def password(self):
        return self['password']

    @password.setter
    def password(self, value):
        self['password'] = salted_hash(value)


class Users(Mapper):

    table = 'users'
    rowcls = User

    find_by_login_sql = 'select * from {self} where login = %(p0)s'


class Session(Row):

    fields = frozenset(('user_id', 'expires'))

    def _new(self):
        self['id'] = b64encode(uuid4().bytes)
        self['expires'] = datetime.utcnow() + config.session_ttl


class Sessions(Mapper):

    table = 'sessions'
    rowcls = Session

    find_sql = '''
        select * from {self} where {pk} = %(p0)s and utc_timestamp() < expires
    '''
