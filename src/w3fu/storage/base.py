from pymongo import Connection

from w3fu import config


class Storage(object):

    def __init__(self, collections):
        self._connection = Connection(config.db_host, config.db_port)
        self._db = self._connection[config.db_name]
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
