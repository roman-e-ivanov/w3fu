from w3fu.storage import StorageError


class Query(object):

    def __init__(self, pattern, params={}):
        self.pattern = pattern
        self.params = params

    def _op(self, other, op):
        params = self.params.copy()
        params.update(other.params)
        return Query('({0} {1} {2})'.format(self.pattern, op, other.pattern), params)

    def __and__(self, other):
        return self._logical_op(other, 'and')

    def __or__(self, other):
        return self._logical_op(other, 'or')


class PropertyQuery(object):

    _key = 0

    def __init__(self, property):
        self._pattern = '{0}.{1}'.format(property.owner.table(), property.name)

    def _op(self, other, op):
        self.__class__._key += 1
        key = 'p{0}'.format(self.__class__._key)
        return Query('{0}{1}%({2})s'.format(self._pattern, op, key), {key: other})

    def __eq__(self, other):
        return self._op(other, '=')

    def __gt__(self, other):
        return self._op(other, '>')

    def __lt__(self, other):
        return self._op(other, '<')

    def __gte__(self, other):
        return self._op(other, '>=')

    def __lte__(self, other):
        return self._op(other, '<=')


class Database(object):

    insert_sql = 'insert ignore into {table} ({keys}) values ({values})'
    update_sql = 'update {table} set {set} where {query}'
    delete_sql = 'delete from {table} where {query}'
    select_sql = 'select {columns} from {table}{join} where {query}'

    def __init__(self, driver, config):
        self._driver = driver
        self._config = config
        self._connect()

    def _connect(self):
        try:
            self._conn = self._driver.connect(**self._config)
        except self._driver.DatabaseError as e:
            raise StorageError(e)

    def _cursor(self):
        try:
            return self._conn.cursor()
        except self._driver.OperationalError:
            self._connect()
            return self._conn.cursor()

    def commit(self):
        try:
            self._conn.commit()
        except self._driver.DatabaseError as e:
            raise StorageError(e)

    def rollback(self):
        try:
            self._conn.rollback()
        except self._driver.DatabaseError as e:
            raise StorageError(e)

    def query(self):
        def make_query(property):
            return PropertyQuery(property)
        return make_query

    def insert(self, entity):
        sql = self.insert_sql.format(table=entity.table(),
                                     keys=','.join(entity.columns),
                                     values=','.join('%({0})s'.format(f)
                                                     for f in entity.columns))
        cursor = self._conn.cursor()
        cursor.execute(sql, dict(entity))
        lastid = cursor.lastrowid
        if lastid and entity.auto is not None:
            entity[entity.auto] = lastid
        return cursor.rowcount

    def update(self, entity):
        sql = self.update_sql.format(table=entity.table(),
                                     set=','.join('{0}=%({0})s'.format(f)
                                                  for f in entity.modified),
                                     query=' and '.join('%0=%({0})s'.format(f)
                                                        for f in entity.pk))
        return self._conn.cursor().execute(sql, dict(entity))

    def delete(self, entitycls, exp):
        sql = self.delete_sql.format(table=entitycls.table(), exp=exp.pattern)
        return self._conn.cursor().execute(sql, exp.params)

    def select(self, entitycls, query=Query('1')):
        tree = [(None, entitycls)]
        for _, cls in tree:
            try:
                tree.extend(zip([cls] * len(cls.join), cls.join.keys()))
            except AttributeError:
                continue
        columns = [(cls, column) for _, cls in tree for column in cls.columns]
        join = ''.join([' left join {0} on ({0}.{1}={2}.{3})'.format(child.table(), child.fk.name, cls.table(), cls.pk.name)
                        for cls, child in tree[1:]])
        sql = self.select_sql.format(
                                     columns=','.join(['{0}.{1}'.format(cls.table(), column)
                                                       for cls, column in columns]),
                                     table=entitycls.table(),
                                     join=join,
                                     query=query.pattern
                                     )
        print(sql)
        cursor = self._conn.cursor()
        cursor.execute(sql, query.params)
        indexed = {}
        ordered = {}
        for row in cursor:
            temp = {}
            for value, (cls, column) in zip(row, columns):
                if value is None:
                    continue
                temp.setdefault(cls, cls())[column] = value
            for cls, entity in temp.iteritems():
                if entity[cls.pk.name] not in indexed.setdefault(cls, {}):
                    indexed[cls][entity[cls.pk.name]] = entity
                    ordered.setdefault(cls, []).append(entity)
        for cls, child in tree[1:]:
            try:
                for entity in ordered[child]:
                    indexed[cls][entity[child.fk.name]].setdefault(cls.join[child], []).append(entity)
            except KeyError:
                continue
        return ordered.get(entitycls, [])
