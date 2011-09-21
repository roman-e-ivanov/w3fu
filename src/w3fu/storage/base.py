from pymongo import Connection


class Storage(object):

    def __init__(self, uri, dbname, collections):
        self._connection = Connection(uri)
        self._db = self._connection[dbname]
        self._collections = {}
        for cls in collections:
            collection = cls(self, self._db[cls.name()])
            collection.ensure_indexes()
            self._collections[cls.name()] = collection

    def __getattr__(self, name):
        try:
            return self._collections[name]
        except KeyError:
            raise AttributeError

    def deref(self, ref):
        return self._db.dereference(ref)

    def free(self):
        self._connection.end_request()
