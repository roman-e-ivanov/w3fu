from w3fu.base import Response
from w3fu.routing import Route
from w3fu.resources import Resource, Form
from w3fu.data.args import StrArg, BoolArg

from app.resources.middleware.transform import json, xml
from app.resources.middleware.context import user


class PlaceSuggestForm(Form):

    pattern = StrArg('pattern', min_size=1, max_size=100, default='')


class PlaceForm(Form):

    name = StrArg('name', min_size=0, max_size=100, default='')
    auto = BoolArg('auto')


class PlaceSuggest(Resource):

    route = Route('/place/suggest')

    @json()
    def get(self, req):
        form = PlaceSuggestForm(req.fs)
        places = self.ctx.storage.places.find_pattern(form.data['pattern'])
        return Response(200, {'found': places})


class Place(Resource):

    route = Route('/place')

    @xml()
    @user()
    def get(self, req):
        resp = Response(200, {'form': PlaceForm(req.fs)})
        if req.fs.getfirst('error') == 'notfound':
            resp.content['error'] = {'notfound': {}}
        return resp

    def post(self, req):
        form = PlaceForm(req.fs, True)
        resp = Response(302)
        if form.err:
            return resp.location(self.route.url(req, form.src))
        if form.data['auto']:
            place = None
            # place = autodetect
        else:
            place = self.ctx.storage.places.find_name(form.data['name'])
        if place is None:
            return resp.location(self.route.url(req, dict(error='notfound', **form.src)))
