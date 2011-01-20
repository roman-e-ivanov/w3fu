# -*- coding: utf-8 -*-

from wsgiref.util import setup_testing_defaults

from w3fu import app


environ = {
           'HTTP_HOST': 'localhost',
           'PATH_INFO': '/login',
           'HTTP_COOKIE': 'u=mgGxNzteT7igDQBqD-OZAw',
           'REQUEST_METHOD': 'GET',
           'QUERY_STRING': u'login=striped&password=8888'
           }

setup_testing_defaults(environ)

def start_response(status, headers):
    print(status)
    for name, value in headers:
        print('%s: %s' % (name, value))

for data in app(environ, start_response):
    print
    print(data)
