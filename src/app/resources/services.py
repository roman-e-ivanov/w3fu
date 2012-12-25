from w3fu.http import OK, Redirect, Forbidden, NotFound
from w3fu.args import StrArg
from w3fu.resources import Resource, Form, HTML
from w3fu.util import class_wrapper

from app.routing import router
from app.view import view
from app.mixins import public_mixins
from app.storage.providers import Provider
from app.storage.services import Service
from app.state import UserState


def paths(service):
    return dict([(name, router[name].path(id_=service.id))
                 for name in ['service_admin']])


class ServiceForm(Form):

    name = StrArg('name', min_size=1, max_size=100)


@class_wrapper(UserState(True))
class ServicesAdmin(Resource):

    html = HTML(view['pages/services-admin'], public_mixins)

    def __call__(self, req, provider_id):
        if not req.user.can_write(provider_id):
            raise Forbidden
        provider = Provider.find_id(provider_id)
        if provider is None:
            raise NotFound
        return super(ServicesAdmin, self).__call__(req, provider)

    @html.GET
    def get(self, req, provider):
        return OK({})

    @html.POST
    @ServiceForm.handler()
    def post(self, req, provider):
        service = Service.new(provider.id, req.form.data['name'])
        Service.insert(service)
        raise Redirect(router['service_admin'] \
                       .url(req, service_id=service.id))


@class_wrapper(UserState(True))
class ServiceAdmin(Resource):

    html = HTML(view['pages/service-admin'], public_mixins)

    def __call__(self, req, service_id):
        service = Service.find_id(service_id)
        if service is None:
            raise NotFound
        if not req.user.can_write(service.provider_id):
            raise Forbidden
        return super(ServiceAdmin, self).__call__(req, service)

    @html.GET
    def get(self, req, service):
        return OK({'service': service})

    @html.PUT
    @ServiceForm.handler()
    def put(self, req, service):
        service.name = req.form.data['name']
        Service.update(service)
        raise Redirect(router['services_list_admin'] \
                       .url(req, provider_id=service.provider_id))

    @html.DELETE
    def delete(self, req, service):
        Service.remove_id(service.id)
        raise Redirect(router['services_list_admin'] \
                       .url(req, provider_id=service.provider_id))


@class_wrapper(UserState(True))
class ServicesListAdmin(Resource):

    html = HTML(view['pages/services-list-admin'], public_mixins)

    @html.GET
    def get(self, req, provider_id_):
        if not req.user.can_write(provider_id_):
            raise Forbidden
        services = Service.find_provider(provider_id_)
        services_paths = dict([(service.id, paths(service))
                                for service in services])
        return OK({'services': services, 'paths': services_paths})
