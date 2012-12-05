from w3fu.http import OK, Redirect, Forbidden, NotFound
from w3fu.args import StrArg
from w3fu.resources import Resource, Form, HTML

from app.routing import router
from app.view import blocks
from app.storage.auth import User
from app.storage.providers import Provider


class ProvidersPublic(Resource):

    html = HTML(blocks['pages/providers-public'])

    @html.GET
    def get(self, req):
        return OK({})


class ProviderPublic(Resource):

    html = HTML(blocks['pages/provider-public'])

    def __call__(self, req, id_):
        provider = Provider.find_id(id_)
        if provider is None:
            raise NotFound
        return super(ProviderPublic, self).__call__(req, provider=provider)

    @html.GET
    def get(self, req, provider):
        return OK({'provider': provider})


class ProviderForm(Form):

    name = StrArg('name', min_size=1, max_size=100)


class ProvidersAdmin(Resource):

    html = HTML(blocks['pages/providers-admin'])

    @html.GET
    def get(self, req):
        return OK({})

    @html.POST
    @ProviderForm.handler()
    def post(self, req):
        provider = Provider.new(req.form.data['name'])
        Provider.insert(provider)
        User.push_owned(req.user, provider.id)
        raise Redirect(router['provider_admin'].url(req, id_=provider.id))


class ProviderAdmin(Resource):

    html = HTML(blocks['pages/provider-admin'])

    def __call__(self, req, id_):
        if not req.user.can_write(id_):
            raise Forbidden
        provider = Provider.find_id(id_)
        if provider is None:
            raise NotFound
        return super(ProviderAdmin, self).__call__(req, provider=provider)

    @html.GET
    def get(self, req, provider):
        return OK({'provider': provider})

    @html.PUT
    @ProviderForm.handler()
    def put(self, req, provider):
        provider.name = req.form.data['name']
        Provider.update(provider)
        raise Redirect(router['providers_list_admin'].url(req))

    @html.DELETE
    def delete(self, req, provider):
        User.pull_owned(provider.id)
        Provider.remove_id(provider.id)
        raise Redirect(router['providers_list_admin'].url(req))


class ProvidersListAdmin(Resource):

    html = HTML(blocks['pages/providers-list-admin'])

    @html.GET
    def get(self, req):
        providers = Provider.find_from_user(req.user)
        return OK({'providers': providers})
