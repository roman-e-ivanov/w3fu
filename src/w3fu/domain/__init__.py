class Entity(dict):

    index = {}

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    @classmethod
    def _data(cls, *args, **kwargs):
        return dict(*args, **kwargs)

    @classmethod
    def new(cls, *args, **kwargs):
        return cls(None, cls._data(*args, **kwargs))

    @classmethod
    def find(cls, db, id):
        return db.select(cls, id)

    def __init__(self, id, *args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)
        self.id = id

    def put(self, db):
        return db.insert(self)

    def save(self, db):
        return db.update(self)

    def remove(self, db):
        return db.delete(self)

    def dump(self):
        out = dict(self)
        out['id'] = self.id
        return out
