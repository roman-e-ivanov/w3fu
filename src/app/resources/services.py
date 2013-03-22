from w3fu.http import OK, Redirect, Forbidden, NotFound
from w3fu.args import StrArg
from w3fu.resources import Resource, Form, HTML
from w3fu.util import class_wrapper

from app.routing import router
from app.view import view
from app.mixins import public_mixins
from app.state import UserState
from app.storage import providers_c, services_c
from app.storage.services import Service, ServiceGroup


def _group(doc):
    block = doc.dump()
    block['paths'] = dict([(name, router[name].path(group_id=doc.id))
                           for name in ['service_group_admin']])
    return block


def _service(doc):
    block = doc.dump()
    block['paths'] = dict([(name, router[name].path(service_id=doc.id))
                           for name in ['service_admin',
                                        'service_groups_admin',
                                        'service_schedule_admin']])
    block['groups'] = [_group(group) for group in doc.groups]
    return block


class ServiceForm(Form):

    name = StrArg('name', min_size=1, max_size=100)


@class_wrapper(UserState(True))
class ServicesAdmin(Resource):

    html = HTML(view['pages/services-admin'], public_mixins)

    def __call__(self, req, provider_id):
        if not req.user.can_write(provider_id):
            raise Forbidden
        provider = providers_c.find_id(provider_id)
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
        services_c.insert(service)
        raise Redirect(router['service_admin'] \
                       .url(req, service_id=service.id))


@class_wrapper(UserState(True))
class ServiceAdmin(Resource):

    html = HTML(view['pages/service-admin'], public_mixins)

    def __call__(self, req, service_id):
        service = services_c.find_id(service_id)
        if service is None:
            raise NotFound
        if not req.user.can_write(service.provider_id):
            raise Forbidden
        return super(ServiceAdmin, self).__call__(req, service)

    @html.GET
    def get(self, req, service):
        return OK({'service': _service(service)})

    @html.PUT
    @ServiceForm.handler()
    def put(self, req, service):
        service.name = req.form.data['name']
        services_c.update(service)
        raise Redirect(router['services_list_admin'] \
                       .url(req, provider_id=service.provider_id))

    @html.DELETE
    def delete(self, req, service):
        services_c.remove_id(service.id)
        raise Redirect(router['services_list_admin'] \
                       .url(req, provider_id=service.provider_id))


@class_wrapper(UserState(True))
class ServicesListAdmin(Resource):

    html = HTML(view['pages/services-list-admin'], public_mixins)

    @html.GET
    def get(self, req, provider_id):
        if not req.user.can_write(provider_id):
            raise Forbidden
        services = services_c.find_provider(provider_id)
        return OK({'services': [_service(service) for service in services]})


@class_wrapper(UserState(True))
class ServiceGroupsAdmin(Resource):

    html = HTML(view['none'])

    def __call__(self, req, service_id):
        service = services_c.find_id(service_id)
        if service is None:
            raise NotFound
        if not req.user.can_write(service.provider_id):
            raise Forbidden
        return super(ServiceGroupsAdmin, self).__call__(req, service)

    @html.POST
    def post(self, req, service):
        group = ServiceGroup.new()
        services_c.push_group(service, group)
        raise Redirect(router['service_admin'] \
                       .url(req, service_id=service.id))


@class_wrapper(UserState(True))
class ServiceGroupAdmin(Resource):

    html = HTML(view['none'])

    def __call__(self, req, group_id):
        service = services_c.find_group(group_id)
        if service is None:
            raise NotFound
        if not req.user.can_write(service.provider_id):
            raise Forbidden
        return super(ServiceGroupAdmin, self).__call__(req, service, group_id)

    @html.DELETE
    def delete(self, req, service, group_id):
        services_c.pull_group(group_id)
        raise Redirect(router['service_admin'] \
                       .url(req, service_id=service.id))
