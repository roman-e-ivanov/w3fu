from w3fu.web import Response
from w3fu.res import bind, Resource
from w3fu.res.middleware.context import storage, session
from w3fu.res.middleware.transform import xml
from w3fu.domain.firms import Firm


@bind('/firms')
class FirmSearch(Resource):

    @xml()
    @storage()
    @session()
    def get(self, req):
        return Response(200, {})


@bind('/firms/{id}', id='\d+')
class FirmShow(Resource):

    @xml()
    @storage()
    @session()
    def get(self, req):
        firm = Firm.find(self.db, id=req.args['id'])
        if firm is None:
            return Response(404)
        return Response(200, {'firm': firm})


@bind('/admin/firms/{id}', id='\d+')
class FirmAdmin(FirmShow):
    pass
