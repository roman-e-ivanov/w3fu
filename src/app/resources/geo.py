from w3fu.http import Response
from w3fu.routing import Route
from w3fu.resources import Form
from w3fu.data.args import StrArg, BoolArg

from app.resources import Resource
from app.resources.middleware.transform import json, xml
from app.resources.middleware.context import user

from app.storage.geo import Place


class PlaceSuggestForm(Form):

    pattern = StrArg('pattern', min_size=1, max_size=100, default='')


class PlaceForm(Form):

    name = StrArg('name', min_size=0, max_size=100, default='')
    auto = BoolArg('auto')
    error = StrArg('error', default='')


class PlaceSuggest(Resource):

    route = Route('/place/suggest')

    @json()
    def get(self, ctx):
        form = PlaceSuggestForm(ctx.req)
        found = Place.find_pattern(form.data['pattern'])
        return Response.ok({'found': found})


class Place(Resource):

    route = Route('/place')

    @xml()
    @user()
    def get(self, ctx):
        return Response.ok({'form': PlaceForm(ctx.req)})

    def post(self, ctx):
        form = PlaceForm(ctx.req, True)
        if form.err:
            return Response.redirect(self.route.url(ctx.req, form.src))
        if form.data['auto']:
            place = None
            # place = autodetect
        else:
            place = Place.find_name(form.data['name'])
        if place is None:
            form.data['error'] = 'notfound'
            return Response.redirect(self.route.url(ctx.req, form.query()))
