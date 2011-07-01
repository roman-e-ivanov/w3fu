import sys
from openid.consumer.consumer import Consumer, DiscoveryFailure, SUCCESS
from pprint import pprint

from w3fu.res import bind, Resource
from w3fu.res.middleware.context import storage
from w3fu.web import Response


@bind('/openid')
class OpenIdAuth(Resource):

    @storage()
    def get(self, req):
        pprint(req.args, sys.stderr)
        consumer = Consumer(self.app.session, self.app.store)
        info = consumer.complete(req.args, 'http://localhost/profile')
        self.app.session = {}
        if info.status == SUCCESS:
            return Response(200, content="OK")
        return Response(401, 'Unauthorized')

    @storage()
    def post(self, req):
        store = req.db.openidstore
        session = {}
        consumer = Consumer(session, store)
        try:
            authrequest = consumer.begin('openid.yandex.ru/roman.e.ivanov')
            #authrequest = consumer.begin('https://www.google.com/accounts/o8/id')
        except DiscoveryFailure:
            return Response(401, 'Unauthorized')
        url = authrequest.redirectURL('http://localhost',
                                      return_to='http://localhost/profile')
        req.db.commit()
        return Response(302).location(url)
