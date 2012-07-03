class Registry(dict):

    def __init__(self, factory, default_name=''):
        self._factory = factory
        self._default_name = default_name

    def push(self, name=None, *args, **kwargs):
        self[name or self._default_name] = self._factory(*args, **kwargs)

    def pull(self, name=None):
        return self[name or self._default_name]
