from w3fu.web import Response
from w3fu.web.forms import Form, StrArg
from w3fu.res import bind, Resource
from w3fu.res.middleware.context import storage, session
from w3fu.res.middleware.transform import xml
from w3fu.res.home import Home
from w3fu.domain.firms import Firm


@bind('/firms')
class FirmsPublic(Resource):

    @xml()
    @storage()
    @session()
    def get(self, req):
        return Response(200, {})


@bind('/firms/{id}', id='\d+')
class FirmPublic(Resource):

    @xml()
    @storage()
    @session()
    def get(self, req):
        firm = Firm.find(self.db, id=req.args['id'])
        if firm is None:
            return Response(404)
        return Response(200, {'firm': firm})


class FirmCreateForm(Form):

    name = StrArg('name', min_size=4, max_size=32)


@bind('/admin/firms')
class FirmsAdmin(Resource):

    @xml('firms-html')
    @storage()
    @session(required=True)
    def get(self, req):
        return Response(200, {'form': FirmCreateForm(req.fs).dump()})

    @storage()
    @session(required=True)
    def post(self, req):
        resp = Response(302)
        form = FirmCreateForm(req.fs)
        if form.err:
            return resp.location(self.url(form.src))
        firm = Firm.new(name=form.data['name'], owner_id=self.session['user_id'])
        firm.insert(self.db)
        self.db.commit()
        return resp.location(FirmAdmin.url(id=firm['id']))


@bind('/admin/firms/{id}', id='\d+')
class FirmAdmin(Resource):

    @xml()
    @storage()
    @session(required=True)
    def get(self, req):
        firm = Firm.find(self.db, id=req.args['id'])
        if firm is None:
            return Response(404)
        return Response(200, {'firm': firm})
