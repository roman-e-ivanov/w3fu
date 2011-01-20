import uuid
import hashlib


class TaggedCache(object):

    def get_tagged(self, key, tags):
        return self.get(key + '-' + self._make_hash(tags))

    def set_tagged(self, key, value, tags):
        self.set(key + '-' + self._make_hash(tags), value)

    def invalidate(self, tags):
        self.delete_multi(tags)

    def _make_hash(self, tags):
        items = {}
        hasher = hashlib.sha1()
        for key, value in self.get_multi(tags).iteritems():
            if value is None:
                value = str(uuid.uuid4())
                items[key] = value
            hasher.update(value)
        if items:
            self.set_multi(items)
        return hasher.hexdigest()

