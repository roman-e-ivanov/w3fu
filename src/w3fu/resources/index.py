from w3fu.web.base import Response
from w3fu.web.resources import bind, Resource
from w3fu.resources.middleware.context import user
from w3fu.resources.middleware.transform import xml


@bind('/')
class Index(Resource):

    @xml('index-html')
    @user()
    def get(self, app, req):
        return Response(200, {})
