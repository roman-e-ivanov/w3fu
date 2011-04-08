from json import dumps, loads


class Entity(dict):

    index = {}

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    @classmethod
    def new(cls, *args, **kwargs):
        self = cls(None, cls._data())
        self.update(*args, **kwargs)
        return self

    @classmethod
    def _data(cls):
        return {}

    @classmethod
    def load(self, s):
        return loads(s)

    @classmethod
    def find(cls, db, id):
        return db.select(cls, id)

    @classmethod
    def delete(cls, db, id):
        db.delete(cls, id)

    @classmethod
    def exists(cls, db, id):
        return db.count(cls, id) > 0

    def __init__(self, id, *args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)
        self.id = id

    def dump(self):
        return dumps(self, separators=(',', ':'))

    def put(self, db):
        db.insert(self)

    def save(self, db):
        db.update(self)
