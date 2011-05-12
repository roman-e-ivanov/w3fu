from urlparse import urlunsplit
from urllib import urlencode


class Url(object):

    def __init__(self, scheme='http', domain='', path='', args={}):
        self.scheme = scheme
        self.domain = domain
        self.path = path
        self.args = args

    def __str__(self):
        return urlunsplit((self.scheme, self.domain, self.path,
                           urlencode([(k, v.encode('utf-8'))
                                      for k, v in self.args.iteritems()]), ''))
