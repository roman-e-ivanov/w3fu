from pymongo import Connection
from pymongo.son_manipulator import SONManipulator

from w3fu import config


class CollectionInjector(SONManipulator):

    def transform_outgoing(self, son, collection):
        son.c = collection
        return son


class Storage(object):

    def __init__(self, collections):
        self._connection = Connection(config.db_host, config.db_port)
        self.db = self._connection[config.db_name]
        self.db.add_son_manipulator(CollectionInjector())
        for collection in collections:
            collection.ensure_indexes(self)

    def free(self):
        self._connection.end_request()
