import re
from urllib import urlencode


class UnpackError(Exception):

    def __init__(self, errors):
        self._errors = errors
        super(UnpackError, self).__init__()

    def dump(self, format):
        return [error.dump(format) for error in self._errors]


class ArgError(Exception):

    _params = {}

    def dump(self, format):
        return {self.__class__.__name__.lower(): self._params}


class ArgAbsent(ArgError): pass
class ArgSizeError(ArgError): pass
class ArgTypeError(ArgError): pass
class ArgRangeError(ArgError): pass


class Packer(object):

    def __init__(self, **args):
        self._args = args
        self._fields = set()
        for arg in args.itervalues():
            self._fields.update(arg.fields())

    def unpack(self, packed, strict):
        unpacked = {}
        errors = []
        for name, arg in self._args.iteritems():
            try:
                unpacked[name] = arg.unpack(packed, strict)
            except ArgError as e:
                errors.append(e)
        if errors:
            raise UnpackError(errors)
        return unpacked

    def pack(self, unpacked):
        packed = {}
        for name, value in unpacked.iteritems():
            self._args[name].pack(value, packed)
        return packed


class Form(Packer):

    def unpack(self, fs, strict=False):
        packed = dict([(k, fs.getfirst(k).decode('utf-8'))
                       for k in fs.keys()])
        return super(Form, self).unpack(packed, strict)

    def pack(self, **unpacked):
        packed = super(Form, self).pack(unpacked)
        return urlencode([(k, v.encode('utf-8'))
                          for k, v in packed.iteritems()])

    def query(self, fs):
        return urlencode([src for arg in self._args
                          for src in arg.src(fs)])


class SingleArg(object):

    def __init__(self, field, default=None, clear=False):
        self._field = field
        self._default = default
        self._clear = clear

    def unpack(self, packed, strict):
        try:
            return self._unpack(packed[self._name])
        except KeyError:
            if strict:
                raise ArgAbsent
            return self._default

    def src(self, fs):
        return [(self._field, '' if self._clear else fs.getfirst(self._field))]


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

    def __init__(self, field):
        super(BoolArg, self).__init__(field, default=False)

    def _unpack(self, value):
        return value and True or False
