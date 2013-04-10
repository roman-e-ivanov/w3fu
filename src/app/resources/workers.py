from w3fu.http import OK, Redirect, Forbidden, NotFound
from w3fu.args import StrArg, IdArg
from w3fu.resources import Resource, Form, HTML
from w3fu.util import class_wrapper

from app.routing import router
from app.view import view
from app.mixins import public_mixins
from app.state import UserState
from app.storage import providers_c, workers_c, services_c
from app.storage.workers import Worker


def _worker(doc):
    block = doc.dump()
    block['paths'] = dict([(name, router[name].path(worker_id=doc.id))
                           for name in ['worker_admin']])
    return block

def _service_worker(doc, service):
    block = _worker(doc)
    for name in ['worker_admin']:
        block['paths'][name] = router[name].path(worker_id=doc.id,
                                                 service_id=service.id)
    return block


class WorkerForm(Form):

    name = StrArg('name', min_size=1, max_size=100)


class ServiceWorkerForm(Form):

    worker_id = IdArg('worker_id')


@class_wrapper(UserState(True))
class WorkersAdmin(Resource):

    html = HTML(view['pages/workers-admin'], public_mixins)

    def __call__(self, req, provider_id):
        if not req.user.can_write(provider_id):
            raise Forbidden
        provider = providers_c.find_id(provider_id)
        if provider is None:
            raise NotFound
        return super(WorkersAdmin, self).__call__(req, provider)

    @html.GET
    def get(self, req, provider):
        return OK({})

    @html.POST
    @WorkerForm.handler()
    def post(self, req, provider):
        worker = Worker.new(provider.id, req.form.data['name'])
        workers_c.insert(worker)
        raise Redirect(router['worker_admin'] \
                       .url(req, worker_id=worker.id))


@class_wrapper(UserState(True))
class WorkerAdmin(Resource):

    html = HTML(view['pages/worker-admin'], public_mixins)

    def __call__(self, req, worker_id):
        worker = workers_c.find_id(worker_id)
        if worker is None:
            raise NotFound
        if not req.user.can_write(worker.provider_id):
            raise Forbidden
        return super(WorkerAdmin, self).__call__(req, worker)

    @html.GET
    def get(self, req, worker):
        return OK({'worker': _worker(worker)})

    @html.PUT
    @WorkerForm.handler()
    def put(self, req, worker):
        worker.name = req.form.data['name']
        workers_c.update(worker)
        raise Redirect(router['workers_list_admin'] \
                       .url(req, provider_id=worker.provider_id))

    @html.DELETE
    def delete(self, req, worker):
        workers_c.remove_id(worker.id)
        raise Redirect(router['workers_list_admin'] \
                       .url(req, provider_id=worker.provider_id))


@class_wrapper(UserState(True))
class WorkersListAdmin(Resource):

    html = HTML(view['pages/workers-list-admin'], public_mixins)

    @html.GET
    def get(self, req, provider_id):
        if not req.user.can_write(provider_id):
            raise Forbidden
        workers = workers_c.find_provider(provider_id)
        return OK({'workers': [_worker(worker) for worker in workers]})


@class_wrapper(UserState(True))
class ServiceWorkersAdmin(Resource):

    html = HTML(view['pages/service-workers-admin'], public_mixins)

    def __call__(self, req, service_id):
        service = services_c.find_id(service_id)
        if service is None:
            raise NotFound
        if not req.user.can_write(service.provider_id):
            raise Forbidden
        return super(ServiceWorkersAdmin, self).__call__(req, service)

    @html.GET
    def get(self, req, service):
        workers = workers_c.find_for_service(service)
        return OK({'workers': [_service_worker(worker, service)
                               for worker in workers]})

    @html.POST
    @ServiceWorkerForm.handler()
    def post(self, req, service):
        worker = workers_c.find_id(req.form.data['worker_id'])
        if worker is None:
            raise NotFound
        services_c.push_worker(service, worker)
        raise Redirect(router['service_admin'].url(req, service_id=service.id))


@class_wrapper(UserState(True))
class ServiceWorkerAdmin(Resource):

    html = HTML(view['none'])

    def __call__(self, req, service_id, worker_id):
        service = services_c.find_with_worker(service_id, worker_id)
        if service is None:
            raise NotFound
        if not req.user.can_write(service.provider_id):
            raise Forbidden
        return super(ServiceWorkerAdmin, self).__call__(req, service, worker_id)

    @html.DELETE
    def delete(self, req, service, worker_id):
        services_c.pull_worker(service.id, worker_id)
        raise Redirect(router['service_admin'].url(req, service_id=service.id))
