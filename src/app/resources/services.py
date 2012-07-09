from w3fu import args, http, resources, routing

from app.resources.middleware.context import user
from app.resources.middleware.transform import xml

from app.storage import providers, services


def block_service(doc):
    nav = {'main': ServiceAdmin.route.path(id=doc.id)}
    return {'doc': doc, 'nav': nav}


class ServiceForm(resources.Form):

    name = args.StrArg('name', min_size=1, max_size=100)


class ServicesAdmin(resources.Resource):

    route = routing.Route('/home/providers/{id}/services', id=args.IdArg('id'))

    @xml('pages/services-admin/html.xsl')
    @user(required=True)
    def get(self, ctx):
        return http.Response.ok({})

    @xml('pages/services-admin/html.xsl')
    @user(required=True)
    def post(self, ctx):
        provider_id = ctx.args['id']
        provider = providers.Provider.find_id(provider_id)
        if provider is None:
            return http.Response.not_found()
        if not ctx.state['user'].can_write(provider_id):
            return http.Response.forbidden()
        form = ServiceForm(ctx.req)
        if form.errors:
            return http.Response.ok({'form': form})
        service = services.Service.new(provider_id, form.data['name'])
        service.Service.insert(service)
        return http.Response.redirect(ServiceAdmin.route.url(ctx.req,
                                                             id=service.id))


class ServiceAdmin(resources.Resource):

    route = routing.Route('/home/services/{id}', id=args.IdArg('id'))

    @xml('pages/service-admin/html.xsl')
    @user(required=True)
    def get(self, ctx):
        service = services.Service.find_id(ctx.args['id'])
        if service is None:
            return http.Response.not_found()
        return http.Response.ok({'service': service})

    @xml('pages/service-admin/html.xsl')
    @user(required=True)
    def put(self, ctx):
        service = services.Service.find_id(ctx.args['id'])
        if service is None:
            return http.Response.not_found()
        if not ctx.state['user'].can_write(service.provider_id):
            return http.Response.forbidden()
        form = ServiceForm(ctx.req)
        if form.errors:
            return http.Response.ok({'form': form})
        service.name = form.data['name']
        services.Service.update(service)
        location = ServicesListAdmin.route.url(ctx.req, id=service.provider_id)
        return http.Response.redirect(location)

    @user(required=True)
    def delete(self, ctx):
        service = services.Service.find_id(ctx.args['id'])
        if service is None:
            return http.Response.not_found()
        if not ctx.state['user'].can_write(service.provider_id):
            return http.Response.forbidden()
        services.Service.remove_id(service.id)
        location = ServicesListAdmin.route.url(ctx.req, id=service.provider_id)
        return http.Response.redirect(location)


class ServicesListAdmin(resources.Resource):

    route = routing.Route('/home/providers/{id}/services/list',
                          id=args.IdArg('id'))

    @xml('pages/services-list-admin/html.xsl')
    @user(required=True)
    def get(self, ctx):
        found = services.Service.find_provider(ctx.args['id'])
        return http.Response.ok({'services': [block_service(doc)
                                              for doc in found]})
