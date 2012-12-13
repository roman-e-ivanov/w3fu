from random import choice
from string import ascii_letters, digits
from hashlib import sha1
from base64 import urlsafe_b64encode, urlsafe_b64decode
from time import mktime
from json import dumps


SALT_SIZE = 4


def b64e(b):
    return urlsafe_b64encode(b).rstrip('=')


def b64d(s):
    return urlsafe_b64decode(s + '=' * [0, 2, 1][len(s) % 3])


def salted_hash(value, salted=None):
    if salted is None:
        salt = ''.join(choice(ascii_letters + digits) for _ in range(SALT_SIZE))
    else:
        salt = salted[:SALT_SIZE]
    return salt + b64e(sha1(salt + value).digest())


def json_dump(data):
    def default(data):
        try:
            return data.dump()
        except AttributeError:
            pass
        try:
            return b64e(data.binary)
        except AttributeError:
            pass
        try:
            return int(mktime(data.timetuple()))
        except AttributeError:
            pass
        return str(data)
    return dumps(data,
                 indent=4, ensure_ascii=False, default=default).encode('utf-8')


def class_wrapper(decorator):
    def wrapper(cls):
        cls.__call__ = decorator(cls.__call__)
        return cls
    return wrapper


def func_wrapper(decorator):
    def wrapper(original):
        def callback(obj, req, *args, **kwargs):
            return original(req, *args, **kwargs)
        decorated = decorator(callback)
        def f(req, *args, **kwargs):
            return decorated(None, req, *args, **kwargs)
        return f
    return wrapper
