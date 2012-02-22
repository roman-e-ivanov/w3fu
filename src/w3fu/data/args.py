import re


class ArgError(Exception):

    _params = {}

    def dump(self, format):
        return {self.__class__.__name__.lower(): self._params}


class ArgAbsentError(ArgError): pass
class ArgSizeError(ArgError): pass
class ArgTypeError(ArgError): pass
class ArgRangeError(ArgError): pass


class SingleArg(object):

    def __init__(self, field, default=None, clear=False, **custom):
        self._field = field
        self._clear = clear
        self._default = default
        self.custom = custom

    def unpack(self, packed):
        try:
            return self._unpack(packed[self._field])
        except KeyError:
            if self._default is None:
                raise ArgAbsentError
            else:
                return self._default

    def pack(self, value, packed):
        packed[self._field] = '' if self._clear else self._pack(value)

    def fields(self):
        return [self._field]

    def _pack(self, value):
        return str(value)


class StrArg(SingleArg):

    def __init__(self, field, trim=True, pattern=None,
                 min_size=0, max_size=65535, **kwargs):
        super(StrArg, self).__init__(field, **kwargs)
        self._trim = trim
        self._min_size = min_size
        self._max_size = max_size
        self._pattern = None if pattern is None else re.compile(pattern)

    def _unpack(self, value):
        if self._trim:
            s = value.strip()
        if not self._min_size <= len(s) <= self._max_size:
            raise ArgSizeError
        if self._pattern is not None and not self._pattern.match(s):
            raise ArgTypeError
        return s


class IntArg(SingleArg):

    def __init__(self, field, min=0, max=None, **kwargs):
        super(IntArg, self).__init__(field, **kwargs)
        self._min = min
        self._max = max

    def _unpack(self, value):
        try:
            x = int(value)
        except ValueError:
            raise ArgTypeError
        if ((self._min is not None and x < self._min) or
            (self._max is not None and x > self._max)):
            raise ArgRangeError
        return x


class BoolArg(SingleArg):

    def __init__(self, field, **kwargs):
        super(BoolArg, self).__init__(field, default=False, **kwargs)

    def _unpack(self, value):
        return value and True or False
