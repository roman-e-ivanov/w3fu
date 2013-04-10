import re
from bson.objectid import ObjectId

from w3fu import util


class ArgError(Exception):

    def __getitem__(self, name):
        try:
            return getattr(self, name)
        except AttributeError:
            raise KeyError


class ArgAbsentError(ArgError):

    code = 'absent'


class ArgSizeError(ArgError):

    code = 'size'


class ArgTypeError(ArgError):

    code = 'type'


class ArgRangeError(ArgError):

    code = 'range'


class StrArg(object):

    def __init__(self, field, default=None, trim=True, pattern=None,
                 min_size=0, max_size=65535):
        self._field = field
        self._default = default
        self._trim = trim
        self._min_size = min_size
        self._max_size = max_size
        self._pattern = pattern
        self._cpattern = pattern and re.compile(pattern)

    def unpack(self, packed):
        try:
            return self._unpack(packed[self._field])
        except KeyError:
            if self._default is None:
                raise ArgAbsentError
            else:
                return self._default

    def pack(self, value, packed):
        packed[self._field] = self._pack(value)

    def fields(self):
        return [self._field]

    def pattern(self):
        return self._pattern or \
            '.{{0},{1}}'.format(self._min_size, self._max_size)

    def _unpack(self, value):
        s = value.decode('utf-8')
        if self._trim:
            s = s.strip()
        if not self._min_size <= len(s) <= self._max_size:
            raise ArgSizeError
        if self._pattern is not None and not self._cpattern.match(s):
            raise ArgTypeError
        return s

    def _pack(self, value):
        return str(value)


class IntArg(StrArg):

    def __init__(self, field, min=0, max=None, **custom):
        super(IntArg, self).__init__(field, **custom)
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

    def pattern(self):
        return '-?\d+'


class BoolArg(StrArg):

    def __init__(self, field, **custom):
        super(BoolArg, self).__init__(field, default=False, **custom)

    def _unpack(self, value):
        return value and True or False

    def pattern(self):
        return '[01]'


class IdArg(StrArg):

    def __init__(self, field, **custom):
        super(IdArg, self).__init__(field, pattern='[\da-zA-Z_-]{16}',
                                    **custom)

    def _unpack(self, value):
        value = super(IdArg, self)._unpack(value)
        return ObjectId(util.b64d(value.encode('utf-8')))

    def _pack(self, value):
        return util.b64e(value.binary)
