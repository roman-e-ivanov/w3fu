from w3fu.base import Response
from w3fu.routing import Route
from w3fu.data.args import StrArg, IdArg
from w3fu.resources import Form, Resource

from app.resources.middleware.context import user
from app.resources.middleware.transform import xml

from app.storage.providers import Providers
from app.storage.services import Services, Service


def block_service(doc):
    nav = {'main': ServiceAdmin.route.path(id=doc.id)}
    return {'doc': doc, 'nav': nav}


class ServiceForm(Form):

    name = StrArg('name', min_size=1, max_size=100)


class ServicesAdmin(Resource):

    route = Route('/home/providers/{id}/services', id=IdArg('id'))

    @xml('pages/services-admin/html.xsl')
    @user(required=True)
    def get(self, req):
        return Response.ok({})

    @xml('pages/services-admin/html.xsl')
    @user(required=True)
    def post(self, req):
        provider_id = req.ctx.args['id']
        provider = Providers(self.ctx.db).find_id(provider_id)
        if provider is None:
            return Response.not_found()
        if not req.ctx.state['user'].can_write(provider_id):
            return Response.forbidden()
        form = ServiceForm(req)
        if form.errors:
            return Response.ok({'form': form})
        service = Service.new(provider_id, form.data['name'])
        Services(self.ctx.db).insert(service)
        return Response.redirect(ServiceAdmin.route.url(req, id=service.id))


class ServiceAdmin(Resource):

    route = Route('/home/services/{id}', id=IdArg('id'))

    @xml('pages/service-admin/html.xsl')
    @user(required=True)
    def get(self, req):
        service = Services(self.ctx.db).find_id(req.ctx.args['id'])
        if service is None:
            return Response.not_found()
        return Response.ok({'service': service})

    @xml('pages/service-admin/html.xsl')
    @user(required=True)
    def put(self, req):
        services = Services(self.ctx.db)
        service = services.find_id(req.ctx.args['id'])
        if service is None:
            return Response.not_found()
        if not req.ctx.state['user'].can_write(service.provider_id):
            return Response.forbidden()
        form = ServiceForm(req)
        if form.errors:
            return Response.ok({'form': form})
        service.name = form.data['name']
        services.update(service)
        location = ServicesListAdmin.route.url(req, id=service.provider_id)
        return Response.redirect(location)

    @user(required=True)
    def delete(self, req):
        services = Services(self.ctx.db)
        service = services.find_id(req.ctx.args['id'])
        if service is None:
            return Response.not_found()
        if not req.ctx.state['user'].can_write(service.provider_id):
            return Response.forbidden()
        services.remove_id(service.id)
        location = ServicesListAdmin.route.url(req, id=service.provider_id)
        return Response.redirect(location)


def block_services(req, services):
    return [{'service': service,
             'path': ServiceAdmin.route.path(id=service.id)}
            for service in services]


class ServicesListAdmin(Resource):

    route = Route('/home/providers/{id}/services/list', id=IdArg('id'))

    @xml('pages/services-list-admin/html.xsl')
    @user(required=True)
    def get(self, req):
        found = Services(self.ctx.db).find_provider(req.ctx.args['id'])
        return Response.ok({'services': [block_service(doc)
                                         for doc in found]})
