from w3fu.storage.documents import Document, Property


class Provider(Document):

    id = Property('_id')
    owner_id = Property('owner_id')
    name = Property('name')

    def _new(self, owner, name):
        self.owner_id = owner.id
        self.name = name

    def writable_by(self, user):
        return self.owner_id == user.id
