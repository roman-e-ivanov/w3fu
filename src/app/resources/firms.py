from w3fu.base import Response
from w3fu.routing import Route
from w3fu.data.args import StrArg, IdArg
from w3fu.resources import Form, Resource

from app.resources.middleware.context import user
from app.resources.middleware.transform import xml

from app.storage.collections.firms import Firms
from app.storage.documents.firms import Firm


class FirmsPublic(Resource):

    route = Route('/firms')

    @xml('firms-public-html.xsl')
    @user()
    def get(self, req):
        return Response.ok({})


class FirmPublic(Resource):

    route = Route('/firms/{id}', id=IdArg('id'))

    @xml('firm-public-html.xsl')
    @user()
    def get(self, req):
        firm = Firms(self.ctx.db).find_id(req.ctx.args['id'])
        if firm is None:
            return Response.not_found()
        return Response.ok({'firm': firm})


class FirmForm(Form):

    name = StrArg('name', min_size=1, max_size=100)


class FirmsAdmin(Resource):

    route = Route('/home/firms')

    @xml('firms-admin-html.xsl')
    @user(required=True)
    def get(self, req):
        return Response.ok({})

    @xml('firms-admin-html.xsl')
    @user(required=True)
    def post(self, req):
        form = FirmForm(req)
        if form.errors:
            return Response.ok({'form': form})
        firm = Firm.new(name=form.data['name'],
                        owner=req.ctx.state['user'])
        Firms(self.ctx.db).insert(firm)
        return Response.redirect(FirmAdmin.route.url(req, id=firm.id))


class FirmAdmin(Resource):

    route = Route('/home/firms/{id}', id=IdArg('id'))

    @xml('firm-admin-html.xsl')
    @user(required=True)
    def get(self, req):
        firm = Firms(self.ctx.db).find_id(req.ctx.args['id'])
        if firm is None:
            return Response.not_found()
        return Response.ok({'firm': firm})

    @user(required=True)
    def put(self, req):
        form = FirmForm(req)
        if form.errors:
            return Response.ok({'form': form})
        firms = Firms(self.ctx.db)
        firm = firms.find_id(req.ctx.args['id'])
        if firm is not None and firm.writable_by(req.ctx.state['user']):
            firm.name = form.data['name']
            firms.update(firm)
        return Response.redirect(FirmsAdmin.route.url(req))

    @user(required=True)
    def delete(self, req):
        firms = Firms(self.ctx.db)
        firm = firms.find_id(req.ctx.args['id'])
        if firm is not None and firm.writable_by(req.ctx.state['user']):
            firms.remove_id(firm.id)
        return Response.redirect(FirmsAdmin.route.url(req))
