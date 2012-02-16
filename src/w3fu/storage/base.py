from pymongo import Connection


class Database(object):

    def __init__(self, uri, dbname):
        self._connection = Connection(uri)
        self._db = self._connection[dbname]

    def collection(self, name):
        return self._db[name]

    def deref(self, ref):
        return self._db.dereference(ref)

    def free(self):
        self._connection.end_request()
