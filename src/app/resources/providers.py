from w3fu import args, http, routing, resources

from app.resources.middleware.context import user
from app.resources.middleware.transform import xml

from app.resources.workers import WorkersListAdmin
from app.resources.services import ServicesListAdmin

from app.storage import auth, providers


def block_provider(doc):
    nav = {'main': ProviderAdmin.route.path(id=doc.id),
           'workers': WorkersListAdmin.route.path(id=doc.id),
           'services': ServicesListAdmin.route.path(id=doc.id)}
    return {'doc': doc, 'nav': nav}


class ProvidersPublic(resources.Resource):

    route = routing.Route('/providers')

    @xml('pages/providers-public/html.xsl')
    @user()
    def get(self, ctx):
        return http.Response.ok({})


class ProviderPublic(resources.Resource):

    route = routing.Route('/providers/{id}', id=args.IdArg('id'))

    @xml('pages/provider-public/html.xsl')
    @user()
    def get(self, ctx):
        provider = providers.Provider.find_id(ctx.args['id'])
        if provider is None:
            return http.Response.not_found()
        return http.Response.ok({'provider': provider})


class ProviderForm(resources.Form):

    name = args.StrArg('name', min_size=1, max_size=100)


class ProvidersAdmin(resources.Resource):

    route = routing.Route('/home/providers')

    @xml('pages/providers-admin/html.xsl')
    @user(required=True)
    def get(self, ctx):
        return http.Response.ok({})

    @xml('pages/providers-admin/html.xsl')
    @user(required=True)
    def post(self, ctx):
        form = ProviderForm(ctx.req)
        if form.errors:
            return http.Response.ok({'form': form})
        provider = providers.Provider.new(form.data['name'])
        providers.Provider.insert(provider)
        auth.User.push_owned(ctx.state['user'], provider.id)
        return http.Response.redirect(ProviderAdmin.route.url(ctx.req,
                                                              id=provider.id))


class ProviderAdmin(resources.Resource):

    route = routing.Route('/home/providers/{id}', id=args.IdArg('id'))

    @xml('pages/provider-admin/html.xsl')
    @user(required=True)
    def get(self, ctx):
        provider = providers.Provider.find_id(ctx.args['id'])
        if provider is None:
            return http.Response.not_found()
        return http.Response.ok({'provider': block_provider(provider)})

    @xml('pages/provider-admin/html.xsl')
    @user(required=True)
    def put(self, ctx):
        provider = providers.Provider.find_id(ctx.args['id'])
        if provider is None:
            return http.Response.not_found()
        if not ctx.state['user'].can_write(provider.id):
            return http.Response.forbidden()
        form = ProviderForm(ctx.req)
        if form.errors:
            return http.Response.ok({'form': form})
        provider.name = form.data['name']
        providers.Provider.update(provider)
        return http.Response.redirect(ProvidersListAdmin.route.url(ctx.req))

    @user(required=True)
    def delete(self, ctx):
        provider = providers.Provider.find_id(ctx.args['id'])
        if provider is None:
            return http.Response.not_found()
        if not ctx.state['user'].can_write(provider.id):
            return http.Response.forbidden()
        auth.User.pull_owned(provider.id)
        providers.Provider.remove_id(provider.id)
        return http.Response.redirect(ProvidersListAdmin.route.url(ctx.req))


class ProvidersListAdmin(resources.Resource):

    route = routing.Route('/home/providers/list')

    @xml('pages/providers-list-admin/html.xsl')
    @user(required=True)
    def get(self, ctx):
        found = providers.Provider.find_from_user(ctx.state['user'])
        return http.Response.ok({'providers': [block_provider(doc)
                                               for doc in found]})
