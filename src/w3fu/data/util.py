from random import choice
from string import ascii_letters, digits
from hashlib import sha1
from base64 import urlsafe_b64encode, urlsafe_b64decode


SALT_SIZE = 4


def b64encode(b):
    return urlsafe_b64encode(b).rstrip('=')

def b64decode(s):
    return urlsafe_b64decode(s + '=' * [0, 2, 1][len(s) % 3])

def salted_hash(value, salted=None):
    if salted is None:
        salt = ''.join(choice(ascii_letters + digits) for _ in range(SALT_SIZE))
    else:
        salt = salted[:SALT_SIZE]
    return salt + b64encode(sha1(salt + value).digest())
