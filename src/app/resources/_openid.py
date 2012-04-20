import sys
from openid.consumer.consumer import Consumer, DiscoveryFailure, SUCCESS
from pprint import pprint

from w3fu.web.resources import bind, Resource
from w3fu.resources.middleware.context import storage
from w3fu.web.base import Response


@bind('/openid')
class OpenIdAuth(Resource):

    @storage()
    def get(self, ctx):
        pprint(ctx.args, sys.stderr)
        consumer = Consumer(self.app.session, self.app.store)
        info = consumer.complete(ctx.args, 'http://localhost/profile')
        self.app.session = {}
        if info.status == SUCCESS:
            return Response(200, content="OK")
        return Response(401, 'Unauthorized')

    @storage()
    def post(self, ctx):
        store = ctx.db.openidstore
        session = {}
        consumer = Consumer(session, store)
        try:
            authrequest = consumer.begin('openid.yandex.ru/roman.e.ivanov')
            #authrequest = consumer.begin('https://www.google.com/accounts/o8/id')
        except DiscoveryFailure:
            return Response(401, 'Unauthorized')
        url = authrequest.redirectURL('http://localhost',
                                      return_to='http://localhost/profile')
        ctx.db.commit()
        return Response(302).location(url)
