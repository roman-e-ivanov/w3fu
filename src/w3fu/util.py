class RegistryMixin(object):

    @classmethod
    def push(cls, key='', *args, **kwargs):
        try:
            instances = cls._instances
        except AttributeError:
            instances = cls._instances = {}
        instances[key] = cls(*args, **kwargs)

    @classmethod
    def pull(cls, key=''):
        return cls._instances[key]
