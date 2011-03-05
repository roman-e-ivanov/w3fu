class Row(dict):

    pk = 'id'

    @classmethod
    def new(cls, *args, **kwargs):
        self = cls(*args, **kwargs)
        self._new()
        return self

    def _new(self):
        pass

    def __setitem__(self, key, value):
        super(Row, self).__setitem__(key, value)
        try:
            self.modified.add(key)
        except AttributeError:
            self.modified = set([key])

    @property
    def id(self):
        try:
            return self[self.pk]
        except KeyError:
            return None

    @id.setter
    def id(self, value):
        super(Row, self).__setitem__(self.pk, value)
