from w3fu.res import bind, Resource
from w3fu.res.snippets import html, user


@bind('/')
class Index(Resource):

    @html('index-html')
    @user
    def get(self):
        return self.req.response(200, {})
