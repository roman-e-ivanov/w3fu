import memcache

from w3fu.data.cache.tags import TaggedCache


class Memcache(TaggedCache):

    def __init__(self, servers):
        self._client = memcache.Client(servers)
