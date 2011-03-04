from w3fu.res import bind, Resource
from w3fu.res.middleware.context import Storage, Logged
from w3fu.res.middleware.transform import XML


@bind('/')
class Index(Resource):

    @XML('index-html')
    @Storage()
    @Logged()
    def get(self, req):
        return req.response(200, {})
