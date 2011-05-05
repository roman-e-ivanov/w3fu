def c(sql):
    def f(cls, db, **args):
        cursor = db.cursor()
        cursor.execute(sql.format(self=cls.name()), args)
        return cursor.fetchone()[0]
    return classmethod(f)

def r(sql, single=False, wrap=True):
    def f(cls, db, **args):
        cursor = db.cursor()
        cursor.execute(sql.format(self=cls.name()), args)
        rows = [cls(row) for row in cursor] if wrap else cursor.fetchall()
        if single:
            return rows[0] if rows else None
        return rows
    return classmethod(f)

def w(sql):
    def f(cls, db, **args):
        cursor = db.cursor()
        return cursor.execute(sql.format(self=cls.name()), args)
    return classmethod(f)


class Entity(dict):

    def __setitem__(self, key, value):
        super(Entity, self).__setitem__(key, value)
        try:
            self.modified.add(key)
        except AttributeError:
            self.modified = set([key])

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    @classmethod
    def new(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    find = r('select * from {self} where id=%(id)s', True)
    delete = w('delete from {self} where id=%(id)s')

    @classmethod
    def find_many(cls, db, ids, sorted=False):
        sql = 'select * from {self} where id in {ids}'
        sql = sql.format(self=cls.name(), ids=','.join(['%s'] * len(ids)))
        cursor = db.cursor()
        cursor.execute(sql, sql.format(cls.name()))
        entities = {}
        for row in cursor:
            entities[row['id']] = cls(row)
        if sorted:
            return [entities[id] for id in ids]
        else:
            return entities.values()

    def insert(self, db):
        sql = 'insert ignore into {self} ({keys}) values ({values})'
        sql = sql.format(self=self.name(),
                         keys=','.join(self.keys()),
                         values=','.join('%({0})s'.format(k) for k in self.keys()))
        cursor = db.cursor()
        count = cursor.execute(sql, dict(self))
        if count:
            self['id'] = cursor.lastrowid
        return count

    def update(self, db):
        sql = 'update {self} set {set} where id=%(id)s'
        sql = sql.format(self=self.table,
                         set=','.join('{0}=%({0})s'.format(f) for f in self.modified))
        cursor = db.cursor()
        return cursor.execute(sql, dict(self.modified))
