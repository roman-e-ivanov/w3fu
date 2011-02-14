from urlparse import urlunsplit
from urllib import urlencode


class Url(object):

    def __init__(self, domain, path='', args={}, scheme='http'):
        self.scheme = scheme
        self.domain = domain
        self.path = path
        self.args = args

    def __str__(self):
        return urlunsplit((self.scheme,
                           self.domain,
                           self.path,
                           urlencode(self.args),
                           ''))
