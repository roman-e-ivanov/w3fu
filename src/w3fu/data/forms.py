class ArgError(Exception):

    @classmethod
    def name(cls):
        return cls.__name__.lower()


class ArgAbsent(ArgError): pass
class ArgSizeError(ArgError): pass
class ArgTypeError(ArgError): pass
class ArgRangeError(ArgError): pass


class FormMeta(type):

    def __init__(cls, name, bases, attrs):
        cls.args = {}
        for name, attr in attrs.iteritems():
            if hasattr(attr, 'is_arg'):
                cls.args[name] = attr
        super(FormMeta, cls).__init__(name, bases, attrs)


class Form(object):

    __metaclass__ = FormMeta

    def __init__(self, raw):
        self.raw = raw
        self.values = {}
        self.errors = {}
        self._validate()

    def content(self):
        return {
                'values': self.raw,
                'errors': self.errors
                }

    def _validate(self):
        for name, arg in self.args.iteritems():
            arg.validate(name, self.raw, self)


class Arg(object):

    is_arg = 1

    def __init__(self, default=None, min_size=0, max_size=65535):
        self._default = default
        self._min_size = min_size
        self._max_size = max_size

    def validate(self, name, raw, form):
        try:
            form.values[name] = self._process(name, raw)
        except ArgAbsent as e:
            if self._default is not None:
                form.values[name] = self._default
            else:
                for field in e.args:
                    form.errors[field] = {e.name(): {}}
        except ArgError as e:
            for field in e.args:
                form.errors[field] = {e.name(): {}}

    def _process(self, name, raw):
        try:
            s = raw[name]
        except KeyError:
            raise ArgAbsent(name)
        if len(s) < self._min_size or len(s) > self._max_size:
            raise ArgSizeError(name)
        return s


class IntArg(Arg):

    def __init__(self, min=0, max=None, **kwargs):
        super(IntArg, self).__init__(**kwargs)
        self._min = min
        self._max = max

    def _process(self, name, raw):
        s = super(IntArg, self)._process(name, raw)
        try:
            x = int(s)
        except ValueError:
            raise ArgTypeError(name)
        if ((self._min is not None and x < self._min) or
            (self._max is not None and x > self._max)):
            raise ArgRangeError(name)
        return x
