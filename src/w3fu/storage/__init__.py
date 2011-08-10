from pymongo import Connection

from w3fu import config


class Storage(object):

    def __init__(self, collections):
        self._connection = Connection(config.db_host, config.db_port)
        self.db = self._connection[config.db_name]
        for collection in collections:
            collection.ensure_indexes(self)

    def free(self):
        self._connection.end_request()
