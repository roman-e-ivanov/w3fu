from w3fu.storage.documents import Document, Property


class Firm(Document):

    id = Property('_id')
    owner_id = Property('owner_id')
    name = Property('name')

    def _new(self, owner, name):
        self.owner_id = owner.id
        self.name = name