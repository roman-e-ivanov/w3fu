from pymongo.errors import PyMongoError, AutoReconnect


class StorageError(Exception): pass


def storagemethod(handler):
    def f(*args, **kwargs):
        many = False
        while True:
            try:
                return handler(*args, **kwargs)
            except AutoReconnect as e:
                if many:
                    raise StorageError(e)
                many = True
            except PyMongoError as e:
                raise StorageError(e)
    return f
