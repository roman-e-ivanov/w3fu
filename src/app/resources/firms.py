from w3fu.web.base import Response
from w3fu.web.forms import Form
from w3fu.web.args import StrArg
from w3fu.web.resources import Route, Resource

from app.resources.middleware.context import user
from app.resources.middleware.transform import xml


class FirmsPublic(Resource):

    route = Route('/firms')

    @xml()
    @user()
    def get(self, req):
        return Response(200, {})


class FirmPublic(Resource):

    route = Route('/firms/{id}', id='\d+')

    @xml()
    @user()
    def get(self, req):
        firm = Firm.find(req.db, id=req.args['id'])
        if firm is None:
            return Response(404)
        return Response(200, {'firm': firm})


class FirmCreateForm(Form):

    name = StrArg('name', min_size=1, max_size=100)


class FirmsAdmin(Resource):

    route = Route('/admin/firms')

    @xml('firms-html.xsl')
    @user(required=True)
    def get(self, req):
        return Response(200, {'form': FirmCreateForm(req.fs).dump()})

    @user(required=True)
    def post(self, req):
        resp = Response(302)
        form = FirmCreateForm(req.fs)
        if form.err:
            return resp.location(self.url(req, form.src))
        firm = Firm.new(name=form.data['name'], owner_id=req.session['user_id'])
        firm.insert(req.db)
        req.db.commit()
        return resp.location(FirmAdmin.url(req, id=firm['id']))


class FirmAdmin(Resource):

    route = Route('/admin/firms/{id}', id='\d+')

    @xml()
    @user(required=True)
    def get(self, req):
        firm = Firm.find(req.db, id=req.args['id'])
        if firm is None:
            return Response(404)
        return Response(200, {'firm': firm})
