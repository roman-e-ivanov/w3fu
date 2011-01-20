from w3fu.res import bind, Resource
from w3fu.res.snippets import html


@bind('/')
class Index(Resource):

    @html('index-html')

    def get(self):
        return self.req.response(200, {})
