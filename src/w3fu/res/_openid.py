import sys
from openid.consumer.consumer import Consumer, DiscoveryFailure, SUCCESS
from pprint import pprint

from w3fu.res import bind, Resource
from w3fu.res.snippets import storage


@bind('/openid')
class OpenIdAuth(Resource):

    @storage
    def get(self, db):
        pprint(self.req.qargs, sys.stderr)
        consumer = Consumer(self.app.session, self.app.store)
        info = consumer.complete(self.req.qargs, 'http://localhost/profile')
        self.app.session = {}
        if info.status == SUCCESS:
            return self.req.response(200, content="OK")
        return self.req.response(401, 'Unauthorized')

    @storage
    def post(self, db):
        store = db.openidstore
        session = {}
        consumer = Consumer(session, store)
        try:
            authrequest = consumer.begin('openid.yandex.ru/roman.e.ivanov')
            #authrequest = consumer.begin('https://www.google.com/accounts/o8/id')
        except DiscoveryFailure:
            return self.req.response(401, content='Unauthorized')
        url = authrequest.redirectURL('http://localhost',
                                      return_to='http://localhost/profile')
        db.commit()
        return self.req.response(302).location(url)
