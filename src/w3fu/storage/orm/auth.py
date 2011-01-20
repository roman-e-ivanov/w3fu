from uuid import uuid4
from base64 import urlsafe_b64encode

from w3fu.storage.orm import Mapper, Row


class Session(Row):

    def new(self):
        self['id'] = urlsafe_b64encode(uuid4().bytes).rstrip('=')


class Sessions(Mapper):

    table = 'sessions'
    rowcls = Session

    insert_sql = '''
        insert ignore into %(self)s (id, user_id, expires) values
        (%%(id)s, %%(user_id)s, from_unixtime(unix_timestamp() + %(ttl)d))
    '''

    find_sql = 'select * from %(self)s where %(pk)s = %%(p0)s and now() < expires'

    def insert(self, row, ttl, sql=insert_sql):
        row.new()
        sql %= {
                'self': self.table,
                'ttl': ttl
                }
        return self._conn.cursor().query(sql, dict(row))


class User(Row):

    def check_password(self, password):
        return self['password'] == password


class Users(Mapper):

    table = 'users'
    rowcls = User

    find_by_login_sql = 'select * from %(self)s where login = %%(p0)s'


class OpenIDStore(Mapper):

    def storeAssociation(self, server_url, association):
        pass

    def getAssociation(self, server_url, handle=None):
        pass

    def removeAssociation(self, server_url, handle):
        pass

    def useNonce(self, server_url, timestamp, salt):
        pass
