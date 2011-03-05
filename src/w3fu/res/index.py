from w3fu.web import Response
from w3fu.res import bind, Resource
from w3fu.res.middleware.context import storage, user
from w3fu.res.middleware.transform import xml


@bind('/')
class Index(Resource):

    @xml('index-html')
    @storage()
    @user()
    def get(self, req):
        return Response(200, {})
