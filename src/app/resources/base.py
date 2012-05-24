from w3fu.resources import Resource


class BaseResource(Resource):

    def _extra(self, data):
        data['user'] = self.rc.state['user']

    def get(self, ctx):
        return self._ok({})
