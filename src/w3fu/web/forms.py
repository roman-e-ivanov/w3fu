import re
from urllib import urlencode


class ArgError(Exception):

    _params = {}

    def dump(self, format):
        return {self.__class__.__name__.lower(): self._params}


class ArgAbsentError(ArgError): pass
class ArgSizeError(ArgError): pass
class ArgTypeError(ArgError): pass
class ArgRangeError(ArgError): pass


class FormMeta(type):

    def __init__(cls, name, bases, attrs):
        cls.args = {}
        for name, attr in attrs.iteritems():
            if hasattr(attr, 'unpack'):
                cls.args[name] = attr
        super(FormMeta, cls).__init__(name, bases, attrs)


class Form(object):

    __metaclass__ = FormMeta

    def __init__(self, fs, strict=False):
        self.data = {}
        self.errors = {}
        self._unpack(self._decode(fs), strict)

    def dump(self, format=None):
        return {'data': self.data, 'errors': self.errors}

    def query(self):
        return self._encode(self._pack())

    def _pack(self):
        packed = {}
        for name, value in self.data.iteritems():
            self.args[name].pack(value, packed)
        return packed

    def _unpack(self, packed, strict):
        for name, arg in self.args.iteritems():
            try:
                self.data[name] = arg.unpack(packed)
            except ArgAbsentError as e:
                if strict:
                    self.errors[name] = e
                else:
                    self.data[name] = None
            except ArgError as e:
                self.errors[name] = e

    def _encode(self, packed):
        return urlencode([(k, v.encode('utf-8'))
                          for k, v in packed.iteritems()])

    def _decode(self, fs):
        return dict([(k, fs.getfirst(k).decode('utf-8'))
                     for k in fs.keys()])


class SingleArg(object):

    def __init__(self, field, default=None, clear=False):
        self._field = field
        self._clear = clear
        self._default = default

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

    def __init__(self, field):
        super(BoolArg, self).__init__(field, default=False)

    def _unpack(self, value):
        return value and True or False
