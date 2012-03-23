from w3fu.base import Response
from w3fu.routing import Route
from w3fu.data.args import StrArg, IdArg
from w3fu.resources import Form, Resource

from app.resources.middleware.context import user
from app.resources.middleware.transform import xml, json

from app.storage.collections.firms import Firms
from app.storage.documents.firms import Firm


class FirmsPublic(Resource):

    route = Route('/firms')

    @xml()
    @user()
    def get(self, req):
        return Response.ok({})


class FirmPublic(Resource):

    route = Route('/firms/{id}', id=IdArg('id'))

    @json()
    @user()
    def get(self, req):
        firms = Firms(self.ctx.db)
        firm = firms.find_id(req.ctx.args['id'])
        if firm is None:
            return Response.not_found()
        return Response.ok({'firm': firm})


class FirmCreateForm(Form):

    name = StrArg('name', min_size=1, max_size=100)


class FirmsAdmin(Resource):

    route = Route('/admin/firms')

    @xml()
    @user(required=True)
    def get(self, req):
        return Response.ok({})

    @xml()
    @user(required=True)
    def post(self, req):
        form = FirmCreateForm(req)
        if form.errors:
            return Response.ok({'form': form})
        firm = Firm.new(name=form.data['name'],
                        owner=req.ctx.state['user'])
        firms = Firms(self.ctx.db)
        firms.insert(firm)
        return Response.redirect(FirmAdmin.route.url(req, id=firm.id))


class FirmAdmin(Resource):

    route = Route('/admin/firms/{id}', id=IdArg('id'))

    @xml()
    @user(required=True)
    def get(self, req):
        firms = Firms(self.ctx.db)
        firm = firms.find_id(req.ctx.args['id'])
        if firm is None:
            return Response.not_found()
        return Response.ok({'firm': firm})
