from bson import ObjectId

from w3fu.storage import safe, Collection, Document, Property, ID, \
    Container, ListContainer

from app.storage.schedule import Schedule
from app.storage.workers import Worker


class ServiceGroup(Document):

    id = ID()

    def _new(self):
        self.id = ObjectId()


class Service(Document):

    id = ID()
    provider_id = ID('provider_id', hidden=True)
    name = Property('name')
    schedule = Container('schedule', Schedule)
    workers = ListContainer('workers', Worker)
    groups = ListContainer('groups', ServiceGroup)

    def _new(self, provider_id, name):
        self.provider_id = provider_id
        self.name = name
        self.schedule = Schedule.new()
        self.groups = [ServiceGroup.new()]

    @property
    def worker_ids(self):
        return [worker.id for worker in self.workers]


class Services(Collection):

    _indexes = [('provider_id', {}),
                ('workers._id', {}),
                ('groups._id', {})]

    @safe()
    def update(self, service):
        return self._c.update({'_id': service.id},
                              {'$set': {'name': service.name}})

    @safe()
    def update_schedule(self, service):
        return self._c.update({'_id': service.id},
                              {'$set': {'schedule': service.schedule.raw}})

    @safe(True)
    def find_provider(self, provider_id):
        return self._c.find({'provider_id': provider_id})

    @safe(True)
    def find_with_worker(self, service_id, worker_id):
        return self._c.find_one({'_id': service_id, 'workers._id': worker_id})

    @safe()
    def push_worker(self, service, worker):
        self._c.update({'_id': service.id, 'workers._id': {'$ne': worker.id}},
                       {'$push': {'workers': worker.embedded}})

    @safe()
    def pull_worker(self, service_id, worker_id):
        self._c.update({'_id': service_id},
                       {'$pull': {'workers': {'_id': worker_id}}})

    @safe(True)
    def find_group(self, group_id):
        return self._c.find_one({'groups._id': group_id})

    @safe()
    def pull_group(self, group_id):
        self._c.update({'groups._id': group_id},
                       {'$pull': {'groups': {'_id': group_id}}})

    @safe()
    def push_group(self, service, group):
        self._c.update({'_id': service.id},
                       {'$push': {'groups': group.raw}})
