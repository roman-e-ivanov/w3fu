from w3fu.http import OK, Redirect, Forbidden, NotFound
from w3fu.args import StrArg
from w3fu.resources import Resource, Form, HTML
from w3fu.util import class_wrapper

from app.routing import router
from app.view import view
from app.mixins import public_mixins
from app.storage.providers import Provider
from app.storage.workers import Worker
from app.state import UserState


def paths(worker):
    return dict([(name, router[name].path(id_=worker.id))
                 for name in ['worker_admin']])


class WorkerForm(Form):

    name = StrArg('name', min_size=1, max_size=100)


@class_wrapper(UserState(True))
class WorkersAdmin(Resource):

    html = HTML(view['pages/workers-admin'], public_mixins)

    def __call__(self, req, provider_id):
        if not req.user.can_write(provider_id):
            raise Forbidden
        provider = Provider.find_id(provider_id)
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
        Worker.insert(worker)
        raise Redirect(router['worker_admin'] \
                       .url(req, worker_id=worker.id))


@class_wrapper(UserState(True))
class WorkerAdmin(Resource):

    html = HTML(view['pages/worker-admin'], public_mixins)

    def __call__(self, req, worker_id):
        worker = Worker.find_id(worker_id)
        if worker is None:
            raise NotFound
        if not req.user.can_write(worker.provider_id):
            raise Forbidden
        return super(WorkerAdmin, self).__call__(req, worker)

    @html.GET
    def get(self, req, worker):
        return OK({'worker': worker})

    @html.PUT
    @WorkerForm.handler()
    def put(self, req, worker):
        worker.name = req.form.data['name']
        Worker.update(worker)
        raise Redirect(router['workers_list_admin'] \
                       .url(req, provider_id=worker.provider_id))

    @html.DELETE
    def delete(self, req, worker):
        Worker.remove_id(worker.id)
        raise Redirect(router['workers_list_admin'] \
                       .url(req, provider_id=worker.provider_id))


@class_wrapper(UserState(True))
class WorkersListAdmin(Resource):

    html = HTML(view['pages/workers-list-admin'], public_mixins)

    @html.GET
    def get(self, req, provider_id):
        if not req.user.can_write(provider_id):
            raise Forbidden
        workers = Worker.find_provider(provider_id)
        workers_paths = dict([(worker.id, paths(worker))
                                for worker in workers])
        return OK({'workers': workers, 'paths': workers_paths})
