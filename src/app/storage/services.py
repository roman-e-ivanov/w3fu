from bson import ObjectId

from w3fu.storage import safe, Collection, Document, Property, ListContainer


class ServiceGroup(Document):

    id = Property('_id')

    def _new(self):
        self.id = ObjectId()


class Service(Document):

    id = Property('_id')
    provider_id = Property('provider_id')
    name = Property('name')
    groups = ListContainer('groups', ServiceGroup)

    def _new(self, provider_id, name):
        self.provider_id = provider_id
        self.name = name
        self.groups = [ServiceGroup.new()]


class Services(Collection):

    _indexes = [('provider_id', {}),
                ('groups._id', {})]

    @safe()
    def update(self, service):
        return self._c.update({'_id': service.id},
                              {'$set': {'name': service.name}})

    @safe(True)
    def find_provider(self, provider_id):
        return self._c.find({'provider_id': provider_id})

    @safe(True)
    def find_group(self, group_id):
        return self._c.find({'groups._id': group_id})

    @safe()
    def pull_group(self, group_id):
        self._c.update({'groups._id': group_id},
                       {'$pull': {'groups': {'_id': group_id}}})

    @safe()
    def push_group(self, service, group):
        self._c.update({'_id': service.id},
                       {'$push': {'groups': group.raw}})
