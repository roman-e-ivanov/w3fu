from w3fu.data.cache.tags import TaggedCache


class InternalCache(TaggedCache):

    def __init__(self):
        self._store = {}

    def get(self, key):
        return self._store.get(key)

    def set(self, key, value):
        self._store[key] = value

    def delete(self, key):
        try:
            del(self._store[key])
        except KeyError:
            pass

    def get_multi(self, keys):
        # WRONG
        return self._store.fromkeys(keys)

    def set_multi(self, items):
        self._store.update(items)

    def delete_multi(self, keys):
        for key in keys:
            self.delete(key)
