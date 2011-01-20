class Row(dict):

    pk = 'id'

    @property
    def id(self):
        return self[self.pk]

    @id.setter
    def id(self, value):
        super(Row, self).__setitem__(self.pk, value)

    def __setitem__(self, key, value):
        super(Row, self).__setitem__(key, value)
        try:
            self.modified.add(key)
        except AttributeError:
            self.modified = set([key])


class Mapper(object):

    insert_sql = 'insert ignore into %(self)s (%(keys)s) values (%(values)s)'
    update_sql = 'update %(self)s set %(set)s where %(pk)s=%%(id)s'
    delete_sql = 'delete from %(self)s where %(pk)s = %%(id)s'
    find_sql = 'select * from %(self)s where %(pk)s = %%(p0)s'

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    def __init__(self, conn):
        self._conn = conn

    def __getattr__(self, name):
        try:
            sql = super(Mapper, self).__getattribute__(name + '_sql')
        except KeyError:
            raise AttributeError(name)
        def query(*args, **kwargs):
            return self._query(sql, args, kwargs)
        return query

    def _query(self, sql, args, kwargs):
        sql %= {'self': self.table, 'pk': self.rowcls.pk}
        params = dict(('p%d' % i, arg) for i, arg in enumerate(args))
        params.update(kwargs)
        return self._conn.cursor().query(sql, params, self.rowcls)

    def insert(self, row, setid=True, sql=insert_sql):
        sql %= {
                'self': self.table,
                'keys': ','.join(row.keys()),
                'values': ','.join('%%(%s)s' % f for f in row.iterkeys())
                }
        cursor = self._conn.cursor().query(sql, dict(row))
        if setid and cursor.count:
            row.id = cursor.lastid
        return cursor

    def update(self, row, sql=update_sql):
        sql %= {
                'self': self.table,
                'set': ','.join('%s=%%(%s)s' % (f, f) for f in row.modified),
                'pk': self.rowcls.pk
                }
        return self._conn.cursor().query(sql, dict(row))

    def delete(self, row, sql=delete_sql):
        sql %= {'self': self.table, 'pk': self.rowcls.pk}
        return self._conn.cursor().query(sql, dict(row))
