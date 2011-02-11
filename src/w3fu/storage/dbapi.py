from w3fu.storage import StorageError


class Connection(object):

    def __init__(self, storage, driver, config, mappers):
        self._storage = storage
        self._driver = driver
        self._config = config
        self._connect()
        for mapper in mappers:
            setattr(self, mapper.name(), mapper(self))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if type is None:
            self._storage.push(self)
        else:
            self._conn.close()

    def _connect(self):
        try:
            self._conn = self._driver.connect(**self._config)
        except self._driver.DatabaseError as e:
            raise StorageError(e)

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

    def cursor(self):
        try:
            cursor = self._conn.cursor()
        except self._driver.OperationalError:
            self._connect()
            cursor = self._conn.cursor()
        return Cursor(cursor, self._driver)


class Cursor(object):

    def __init__(self, cursor, driver):
        self._cursor = cursor
        self._driver = driver

    def __iter__(self):
        return self

    def next(self):
        dto = self.fetch()
        if dto is None:
            raise StopIteration
        return dto

    def query(self, sql, params=None, rowcls=None):
        self._rowcls = rowcls
        try:
            self._cursor.execute(sql, params)
        except self._driver.DatabaseError as e:
            raise StorageError(e)
        return self

    def fetch(self):
        row = self._cursor.fetchone()
        if row is None:
            return None
        try:
            return self._rowcls(row)
        except TypeError:
            return row

    @property
    def count(self):
        return self._cursor.rowcount

    @property
    def lastid(self):
        return self._cursor.lastrowid
