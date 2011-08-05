from pymongo import Connection

from w3fu import config


class Database(object):

    def __init__(self, collections):
        self._conn = Connection(config.db_host, config.db_port)
        db = self._conn[config.db_name]
        for collection in collections:
            setattr(self, collection.name(), collection(db))

    def free(self):
        self._conn.end_request()
