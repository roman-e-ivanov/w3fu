from pymongo.errors import PyMongoError, AutoReconnect

from w3fu.storage.errors import StorageError


class Collection(object):

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    def __init__(self, db):
        self._c = db[self.name()]
        self._ensure_index()

    def __getattr__(self, name):
        attr = super(Collection, self).__getattribute__('_' + name)
        def f(*args, **kwargs):
            many = False
            while True:
                try:
                    return attr(*args, **kwargs)
                except AutoReconnect as e:
                    if many:
                        raise StorageError(e)
                    many = True
                except PyMongoError as e:
                    raise StorageError(e)
        return f

    def _ensure_index(self):
        pass
