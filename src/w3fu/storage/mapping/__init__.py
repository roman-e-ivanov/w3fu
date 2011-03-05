class Mapper(object):

    insert_sql = 'insert ignore into {self} ({keys}) values ({values})'
    update_sql = 'update {self} set {set} where {pk}=%(id)s'
    delete_sql = 'delete from {self} where {pk} = %(p0)s'
    find_sql = 'select * from {self} where {pk} = %(p0)s'

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
        sql = sql.format(self=self.table, pk=self.rowcls.pk)
        params = dict(('p{0!s}'.format(i), arg) for i, arg in enumerate(args))
        params.update(kwargs)
        return self._conn.cursor().query(sql, params, self.rowcls)

    def insert(self, row, sql=insert_sql):
        sql = sql.format(self=self.table,
                         keys=','.join(row.keys()),
                         values=','.join('%({0})s'.format(f) for f in row.iterkeys())
                         )
        cursor = self._conn.cursor().query(sql, dict(row))
        if row.id is None and cursor.count and cursor.lastid:
            row.id = cursor.lastid
        return cursor

    def update(self, row, sql=update_sql):
        sql = sql.format(self=self.table,
                         set=','.join('{0}=%({1})s'.format(f, f) for f in row.modified),
                         pk=self.rowcls.pk
                         )
        return self._conn.cursor().query(sql, dict(row))
