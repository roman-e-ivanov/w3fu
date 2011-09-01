from w3fu.web import Response
from w3fu.res import bind, Resource
from w3fu.res.middleware.context import user
from w3fu.res.middleware.transform import xml


@bind('/home')
class Home(Resource):

    @xml('home-html')
    @user()
    def get(self, app, req):
        return Response(200, {})
