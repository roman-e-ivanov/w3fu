from w3fu.http import OK, Redirect, Forbidden, NotFound
from w3fu.args import StrArg
from w3fu.resources import Resource, Form, HTML
from w3fu.util import class_wrapper

from app.routing import router
from app.view import view
from app.mixins import public_mixins
from app.state import UserState
from app.storage import users_c, providers_c
from app.storage.providers import Provider


def paths(provider):
    return dict([(name, router[name].path(provider_id=provider.id))
                 for name in ['provider_public', 'provider_admin',
                              'services_list_admin', 'services_admin',
                              'workers_list_admin', 'workers_admin']])


class ProvidersPublic(Resource):

    html = HTML(view['pages/providers-public'], public_mixins)

    @html.GET
    def get(self, req):
        return OK({})


class ProviderPublic(Resource):

    html = HTML(view['pages/provider-public'], public_mixins)

    def __call__(self, req, provider_id):
        provider = providers_c.find_id(provider_id)
        if provider is None:
            raise NotFound
        return super(ProviderPublic, self).__call__(req, provider)

    @html.GET
    def get(self, req, provider):
        return OK({'provider': provider})


class ProviderForm(Form):

    name = StrArg('name', min_size=1, max_size=100)


@class_wrapper(UserState(True))
class ProvidersAdmin(Resource):

    html = HTML(view['pages/providers-admin'], public_mixins)

    @html.GET
    def get(self, req):
        return OK({})

    @html.POST
    @ProviderForm.handler()
    def post(self, req):
        provider = Provider.new(req.form.data['name'])
        providers_c.insert(provider)
        users_c.push_owned(req.user, provider.id)
        raise Redirect(router['provider_admin'].url(req, provider_id=provider.id))


@class_wrapper(UserState(True))
class ProviderAdmin(Resource):

    html = HTML(view['pages/provider-admin'], public_mixins)

    def __call__(self, req, provider_id):
        if not req.user.can_write(provider_id):
            raise Forbidden
        provider = providers_c.find_id(provider_id)
        if provider is None:
            raise NotFound
        return super(ProviderAdmin, self).__call__(req, provider)

    @html.GET
    def get(self, req, provider):
        return OK({'provider': provider, 'paths': paths(provider)})

    @html.PUT
    @ProviderForm.handler()
    def put(self, req, provider):
        provider.name = req.form.data['name']
        providers_c.update(provider)
        raise Redirect(router['providers_list_admin'].url(req))

    @html.DELETE
    def delete(self, req, provider):
        users_c.pull_owned(provider.id)
        providers_c.remove_id(provider.id)
        raise Redirect(router['providers_list_admin'].url(req))


@class_wrapper(UserState(True))
class ProvidersListAdmin(Resource):

    html = HTML(view['pages/providers-list-admin'], public_mixins)

    @html.GET
    def get(self, req):
        providers = providers_c.find_from_user(req.user)
        providers_paths = dict([(provider.id, paths(provider))
                                for provider in providers])
        return OK({'providers': providers, 'paths': providers_paths})
