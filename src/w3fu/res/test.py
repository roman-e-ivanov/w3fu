from w3fu.res import bind, Resource
from w3fu.res.snippets import html, json


class Test(Resource):

    def get(self):
        return self.req.response(200, {'data': 42})


@bind('/test')
class HtmlTest(Test):

    get = html('test-html')(Test.get)


@bind('/test.json')
class JsonTest(Test):

    get = json(Test.get)
