from w3fu import args, http, resources, routing

from app.resources.middleware.transform import json, xml
from app.resources.middleware.context import user

from app.storage import geo


class PlaceSuggestForm(resources.Form):

    pattern = args.StrArg('pattern', min_size=1, max_size=100, default='')


class PlaceForm(resources.Form):

    name = args.StrArg('name', min_size=0, max_size=100, default='')
    auto = args.BoolArg('auto')
    error = args.StrArg('error', default='')


class PlaceSuggest(resources.Resource):

    route = routing.Route('/place/suggest')

    @json()
    def get(self, ctx):
        form = PlaceSuggestForm(ctx.req)
        found = geo.Place.find_pattern(form.data['pattern'])
        return http.Response.ok({'found': found})


class Place(resources.Resource):

    route = routing.Route('/place')

    @xml()
    @user()
    def get(self, ctx):
        return http.Response.ok({'form': PlaceForm(ctx.req)})

    def post(self, ctx):
        form = PlaceForm(ctx.req, True)
        if form.err:
            return http.Response.redirect(self.route.url(ctx.req, form.src))
        if form.data['auto']:
            place = None
            # place = autodetect
        else:
            place = geo.Place.find_name(form.data['name'])
        if place is None:
            form.data['error'] = 'notfound'
            return http.Response.redirect(self.route.url(ctx.req, form.query()))
