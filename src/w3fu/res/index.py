from w3fu.res import bind, Resource
from w3fu.res.snippets import html, user, storage


@bind('/')
class Index(Resource):

    @html('index-html')
    @storage
    @user
    def get(self, db, user):
        return self.req.response(200, {})
