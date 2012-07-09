import random
import string
import hashlib
import base64
import time
import json


SALT_SIZE = 4


def b64e(b):
    return base64.urlsafe_b64encode(b).rstrip('=')


def b64d(s):
    return base64.urlsafe_b64decode(s + '=' * [0, 2, 1][len(s) % 3])


def salted_hash(value, salted=None):
    if salted is None:
        salt = ''.join(random.choice(string.ascii_letters + string.digits)
                       for _ in range(SALT_SIZE))
    else:
        salt = salted[:SALT_SIZE]
    return salt + b64e(hashlib.sha1(salt + value).digest())


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
            return int(time.mktime(data.timetuple()))
        except AttributeError:
            pass
        return str(data)
    return json.dumps(data, indent=4, ensure_ascii=False,
                      default=default).encode('utf-8')


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
