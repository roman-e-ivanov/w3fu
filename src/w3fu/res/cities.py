from w3fu.web import Response
from w3fu.web.forms import Form, StrArg
from w3fu.res import bind, Resource
from w3fu.res.middleware.transform import json
from w3fu.storage.documents.cities import City


class CitySuggestForm(Form):

    prefix = StrArg('prefix', min_size=1, max_size=100)


@bind('/city-suggest')
class CitySuggest(Resource):

    @json()
    def get(self, app, req):
        form = CitySuggestForm(req.fs)
        cities = City.find_name_prefix(app.storage, form.data.get('prefix', ''))
        return Response(200, {'found': [city.dump('json') for city in cities]})
