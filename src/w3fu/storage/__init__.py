class StorageError(Exception): pass


class Storage(object):

    def __init__(self, dbcls):
        self._dbcls = dbcls
        self._pool = []

    def push(self, conn):
        self._pool.append(conn)

    def pull(self):
        try:
            return self._pool.pop()
        except IndexError:
            return self._dbcls()
