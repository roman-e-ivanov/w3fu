from w3fu.storage import safe, Collection, Document, Property, ID


class Provider(Document):

    id = ID()
    name = Property('name')

    def _new(self, name):
        self.name = name


class Providers(Collection):

    @safe()
    def update(self, provider):
        return self._c.update({'_id': provider.id},
                              {'$set': {'name': provider.name}})

    @safe(True)
    def find_from_user(self, user):
        return self._c.find({'_id': {'$in': user.owned}})
