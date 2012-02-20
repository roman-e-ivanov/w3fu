from w3fu.base import Response
from w3fu.routing import Route
from w3fu.data.args import StrArg
from w3fu.resources import Form, Resource

from app.resources.middleware.context import user
from app.resources.middleware.transform import xml


class FirmsPublic(Resource):

    route = Route('/firms')

    @xml()
    @user()
    def get(self, req):
        return Response.ok({})


class FirmPublic(Resource):

    route = Route('/firms/{id}', id='\d+')

    @xml()
    @user()
    def get(self, req):
        firm = Firm.find(req.db, id=req.args['id'])
        if firm is None:
            return Response.not_found()
        return Response.ok({'firm': firm})


class FirmCreateForm(Form):

    name = StrArg('name', min_size=1, max_size=100)


class FirmsAdmin(Resource):

    route = Route('/admin/firms')

    @xml('firms-html.xsl')
    @user(required=True)
    def get(self, req):
        return Response.ok({'form': FirmCreateForm(req).dump()})

    @user(required=True)
    def post(self, req):
        form = FirmCreateForm(req)
        if form.err:
            return Response.redirect(self.url(req, form.src))
        firm = Firm.new(name=form.data['name'], owner_id=req.session['user_id'])
        firm.insert(req.db)
        req.db.commit()
        return Response.redirect(FirmAdmin.url(req, id=firm['id']))


class FirmAdmin(Resource):

    route = Route('/admin/firms/{id}', id='\d+')

    @xml()
    @user(required=True)
    def get(self, req):
        firm = Firm.find(req.db, id=req.args['id'])
        if firm is None:
            return Response.not_found()
        return Response.ok({'firm': firm})
