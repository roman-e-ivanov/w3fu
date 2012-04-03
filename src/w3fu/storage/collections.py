from pymongo.cursor import Cursor
from pymongo.errors import PyMongoError, AutoReconnect, DuplicateKeyError

from w3fu.storage.errors import StorageError


def errorsafe(method):
    def handler(*args, **kwargs):
        many = False
        while True:
            try:
                return method(*args, **kwargs)
            except AutoReconnect as e:
                if many:
                    raise StorageError(e)
                many = True
            except DuplicateKeyError:
                return False
            except PyMongoError as e:
                raise StorageError(e)
    return handler


def wrapped(method):
    def handler(collection, *args, **kwargs):
        doc_or_docs = method(collection, *args, **kwargs)
        if isinstance(doc_or_docs, Cursor):
            return [collection.load(doc) for doc in doc_or_docs]
        if doc_or_docs is not None:
            return collection.load(doc_or_docs)
        return None
    return handler


class Collection(object):

    _indexes = []

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    def __init__(self, database):
        self._database = database
        self._collection = database.collection(self.name())
        self._ensure_indexes()

    def _ensure_indexes(self):
        for index, kwargs in self._indexes:
            self._collection.ensure_index(index, **kwargs)

    def load(self, raw):
        return self._doc_cls(raw, self)

    @errorsafe
    def insert(self, doc, safe=False):
        self._collection.insert(doc.raw, safe=safe)
        return True

    @errorsafe
    def remove_id(self, id, safe=False):
        return self._collection.remove({'_id': id}, safe=safe)

    @wrapped
    @errorsafe
    def find_id(self, id):
        return self._collection.find_one({'_id': id})
