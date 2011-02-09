import re


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

    def __init__(self, src):
        self.src = dict(src)
        self.err = {}
        self.data = {}
        self._process()

    def content(self):
        return {
                'values': self.src,
                'errors': self.err
                }

    def _process(self):
        for name, arg in self.args.iteritems():
            self.data[name] = arg.process(self.src, self.err)


class Arg(object):

    is_arg = 1

    def __init__(self, name, default=None, clear=False):
        self._name = name
        self._default = default
        self._clear = clear

    def process(self, src, err):
        try:
            try:
                value = src[self._name]
            except KeyError:
                raise ArgAbsent()
            return self._process(value)
        except ArgAbsent as e:
            if self._default is not None:
                return self._default
            err[self._name] = {e.name(): {}}
        except ArgError as e:
            err[self._name] = {e.name(): {}}
        finally:
            if self._clear:
                try:
                    del src[self._name]
                except KeyError:
                    pass
        return None


class StrArg(Arg):

    def __init__(self, name, trim=True, pattern=None,
                 min_size=0, max_size=65535, **kwargs):
        super(StrArg, self).__init__(name, **kwargs)
        self._trim = trim
        self._min_size = min_size
        self._max_size = max_size
        if pattern is not None:
            self._pattern = re.compile(pattern)

    def _process(self, value):
        if self._trim:
            s = value.strip()
        if not self._min_size <= len(s) <= self._max_size:
            raise ArgSizeError()
        try:
            if not self._pattern.match(s):
                raise ArgTypeError()
        except AttributeError:
            pass
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
            raise ArgTypeError()
        if ((self._min is not None and x < self._min) or
            (self._max is not None and x > self._max)):
            raise ArgRangeError()
        return x
