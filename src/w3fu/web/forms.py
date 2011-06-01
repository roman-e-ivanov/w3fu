import re


class ArgError(Exception):

    @classmethod
    def name(cls):
        return cls.__name__.lower()


class ArgSizeError(ArgError): pass
class ArgTypeError(ArgError): pass
class ArgRangeError(ArgError): pass


class FormMeta(type):

    def __init__(cls, name, bases, attrs):
        for name, attr in attrs.iteritems():
            if hasattr(attr, 'attach'):
                attr.attach(name, cls)
        super(FormMeta, cls).__init__(name, bases, attrs)


class Form(object):

    __metaclass__ = FormMeta

    def __init__(self, fs):
        self.src = dict([(k, fs.getfirst(k).decode('utf-8')) for k in fs.keys()])
        self.err = {}
        self.data = {}
        self._process()

    def dump(self):
        return {'source': self.src, 'errors': self.err}

    def _process(self):
        for name, arg in self.args.iteritems():
            self.data[name] = arg.process(self.src, self.err)


class Arg(object):

    def __init__(self, name, clear=False):
        self._name = name
        self._clear = clear

    def attach(self, name, cls):
        if not hasattr(cls, 'args'):
            cls.args = {}
        cls.args[name] = self

    def process(self, src, err):
        try:
            value = src.get(self._name)
            if value is None:
                return None
            return self._process(value)
        except ArgError as e:
            err[self._name] = {e.name(): {}}
        finally:
            if self._clear and value is not None:
                src[self._name] = ''
        return None


class StrArg(Arg):

    def __init__(self, name, trim=True, pattern=None,
                 min_size=0, max_size=65535, **kwargs):
        super(StrArg, self).__init__(name, **kwargs)
        self._trim = trim
        self._min_size = min_size
        self._max_size = max_size
        self._pattern = None if pattern is None else re.compile(pattern)

    def _process(self, value):
        if self._trim:
            s = value.strip()
        if not self._min_size <= len(s) <= self._max_size:
            raise ArgSizeError
        if self._pattern is not None and not self._pattern.match(s):
            raise ArgTypeError
        return s


class IntArg(Arg):

    def __init__(self, name, min=0, max=None, **kwargs):
        super(IntArg, self).__init__(name, **kwargs)
        self._min = min
        self._max = max

    def _process(self, value):
        try:
            x = int(value)
        except ValueError:
            raise ArgTypeError
        if ((self._min is not None and x < self._min) or
            (self._max is not None and x > self._max)):
            raise ArgRangeError
        return x
