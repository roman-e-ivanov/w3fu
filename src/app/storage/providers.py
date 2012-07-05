from w3fu import storage


class Provider(storage.Model):

    _collection = 'providers'

    id = storage.Property('_id')
    name = storage.Property('name')

    def _new(self, name):
        self.name = name

    @classmethod
    @storage.safe()
    def update(cls, provider):
        return cls._c().update({'_id': provider.id},
                               {'$set': {'name': provider.name}})

    @classmethod
    @storage.safe(True)
    def find_from_user(cls, user):
        return cls._c().find({'_id': {'$in': user.owned}})
