import MySQLdb
from MySQLdb.cursors import DictCursor

from w3fu import config
from w3fu.storage import StorageError


class Database(object):

    def __init__(self):
        self._connect()

    def _connect(self):
        try:
            self._conn = MySQLdb.connect(host=config.conn_host,
                                         db=config.conn_db,
                                         user=config.conn_user,
                                         passwd=config.conn_passwd,
                                         use_unicode=True,
                                         charset='utf8',
                                         cursorclass=DictCursor)
        except MySQLdb.DatabaseError as e:
            raise StorageError(e)

    def cursor(self):
        try:
            return self._conn.cursor()
        except MySQLdb.OperationalError:
            self._connect()
            return self._conn.cursor()

    def commit(self):
        try:
            self._conn.commit()
        except MySQLdb.DatabaseError as e:
            raise StorageError(e)

    def rollback(self):
        try:
            self._conn.rollback()
        except MySQLdb.DatabaseError as e:
            raise StorageError(e)
