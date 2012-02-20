from w3fu.base import Response
from w3fu.routing import Route
from w3fu.resources import Resource, Form
from w3fu.data.args import StrArg, BoolArg

from app.resources.middleware.transform import json, xml
from app.resources.middleware.context import user

from app.storage.collections.geo import Places


class PlaceSuggestForm(Form):

    pattern = StrArg('pattern', min_size=1, max_size=100, default='')


class PlaceForm(Form):

    name = StrArg('name', min_size=0, max_size=100, default='')
    auto = BoolArg('auto')
    error = StrArg('error', default='')


class PlaceSuggest(Resource):

    route = Route('/place/suggest')

    @json()
    def get(self, req):
        form = PlaceSuggestForm(req)
        places = Places(self.ctx.db)
        found = places.find_pattern(form.data['pattern'])
        return Response.ok({'found': found})


class Place(Resource):

    route = Route('/place')

    @xml()
    @user()
    def get(self, req):
        return Response.ok({'form': PlaceForm(req)})

    def post(self, req):
        form = PlaceForm(req, True)
        if form.err:
            return Response.redirect(self.route.url(req, form.src))
        if form.data['auto']:
            place = None
            # place = autodetect
        else:
            places = Places(self.ctx.db)
            place = places.find_name(form.data['name'])
        if place is None:
            form.data['error'] = 'notfound'
            return Response.redirect(self.route.url(req, form.query()))
