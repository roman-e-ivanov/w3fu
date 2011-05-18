from w3fu.web import Response
from w3fu.res import bind, Resource
from w3fu.res.middleware.context import storage, session
from w3fu.res.middleware.transform import xml


@bind('/home')
class Home(Resource):

    @xml()
    @storage()
    @session()
    def get(self, req):
        return Response(200, {})
