from uuid import uuid4
from base64 import urlsafe_b64encode

from w3fu.storage.orm import Mapper, Row


class Session(Row):

    fields = frozenset(('user_id', 'expires'))

    def _new(self):
        self.id = urlsafe_b64encode(uuid4().bytes).rstrip('=')


class Sessions(Mapper):

    table = 'sessions'
    rowcls = Session

    insert_sql = '''
        insert ignore into {self} (id, user_id, expires) values
        (%(id)s, %(user_id)s, from_unixtime(unix_timestamp() + {ttl!s}))
    '''

    find_sql = 'select * from {self} where {pk} = %(p0)s and now() < expires'

    def insert(self, row, ttl, sql=insert_sql):
        sql = sql.format(self=self.table, ttl=ttl)
        return self._conn.cursor().query(sql, dict(row))


class User(Row):

    fields = frozenset(('login', 'password'))

    def check_password(self, password):
        return self.password == password


class Users(Mapper):

    table = 'users'
    rowcls = User

    find_by_login_sql = 'select * from {self} where login = %(p0)s'
