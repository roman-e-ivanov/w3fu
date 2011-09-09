from w3fu.web.base import Response
from w3fu.web.forms import Form, StrArg
from w3fu.web.resources import bind, Resource
from w3fu.resources.middleware.transform import json


class PlaceSuggestForm(Form):

    pattern = StrArg('pattern', min_size=1, max_size=100, default='')


@bind('/place-suggest')
class PlaceSuggest(Resource):

    @json()
    def get(self, app, req):
        form = PlaceSuggestForm(req.fs)
        places = app.storage.places.find_pattern(form.data['pattern'])
        return Response(200, {'found': places})
