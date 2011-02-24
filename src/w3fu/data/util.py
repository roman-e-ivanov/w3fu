from random import choice
from string import ascii_letters, digits
from hashlib import sha1
from base64 import urlsafe_b64encode


def b64encode(bytes):
    return urlsafe_b64encode(bytes).rstrip('=')


SALT_SIZE = 4


def salted_hash(value, salted=None):
    if salted is None:
        salt = ''.join(choice(ascii_letters + digits) for _ in range(SALT_SIZE))
    else:
        salt = salted[:SALT_SIZE]
    return salt + b64encode(sha1(salt + value).digest())
