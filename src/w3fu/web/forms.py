import re


class ArgError(Exception):

    _params = {}

    def dump(self, format):
        return {self.__class__.__name__.lower(): self._params}


class ArgAbsent(ArgError): pass
class ArgSizeError(ArgError): pass
class ArgTypeError(ArgError): pass
class ArgRangeError(ArgError): pass


class FormMeta(type):

    def __init__(cls, name, bases, attrs):
        cls.args = {}
        for name, attr in attrs.iteritems():
            if hasattr(attr, 'process'):
                cls.args[name] = attr
        super(FormMeta, cls).__init__(name, bases, attrs)


class Form(object):

    __metaclass__ = FormMeta

    def __init__(self, fs, strict=False):
        self.src = dict([(k, fs.getfirst(k).decode('utf-8')) for k in fs.keys()])
        self.err = {}
        self.data = {}
        for name, arg in self.args.iteritems():
            self.data[name] = arg.process(self.src, self.err, strict)

    def dump(self, format):
        return {'source': self.src, 'errors': self.err}


class Arg(object):

    def __init__(self, name, default=None, clear=False):
        self._name = name
        self._default = default
        self._clear = clear

    def process(self, src, err, strict):
        try:
            return self._process(src[self._name])
        except KeyError:
            if strict:
                err[self._name] = ArgAbsent()
            return self._default
        except ArgError as e:
            err[self._name] = e
        finally:
            if self._clear:
                src[self._name] = ''
        return self._default


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
