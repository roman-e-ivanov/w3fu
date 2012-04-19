from w3fu.base import Response
from w3fu.routing import Route
from w3fu.data.args import StrArg, IdArg
from w3fu.resources import Form, Resource

from app.resources.middleware.context import user
from app.resources.middleware.transform import xml

from app.storage.providers import Providers
from app.storage.workers import Workers, Worker


class WorkerForm(Form):

    name = StrArg('name', min_size=1, max_size=100)


class WorkersAdmin(Resource):

    route = Route('/home/providers/{id}/workers', id=IdArg('id'))

    @xml()
    @user(required=True)
    def get(self, req):
        return Response.ok({})

    @xml()
    @user(required=True)
    def post(self, req):
        provider_id = req.ctx.args['id']
        provider = Providers(self.ctx.db).find_id(provider_id)
        if provider is None:
            return Response.not_found()
        if not req.ctx.state['user'].can_write(provider_id):
            return Response.forbidden()
        form = WorkerForm(req)
        if form.errors:
            return Response.ok({'form': form})
        worker = Worker.new(provider_id, form.data['name'])
        Workers(self.ctx.db).insert(worker)
        return Response.redirect(WorkerAdmin.route.url(req, id=worker.id))


class WorkerAdmin(Resource):

    route = Route('/home/workers/{id}', id=IdArg('id'))

    @xml()
    @user(required=True)
    def get(self, req):
        worker = Workers(self.ctx.db).find_id(req.ctx.args['id'])
        if worker is None:
            return Response.not_found()
        return Response.ok({'worker': worker})

    @xml()
    @user(required=True)
    def put(self, req):
        workers = Workers(self.ctx.db)
        worker = workers.find_id(req.ctx.args['id'])
        if worker is None:
            return Response.not_found()
        if not req.ctx.state['user'].can_write(worker.provider_id):
            return Response.forbidden()
        form = WorkerForm(req)
        if form.errors:
            return Response.ok({'form': form})
        worker.name = form.data['name']
        workers.update(worker)
        location = WorkersListAdmin.route.url(req, id=worker.provider_id)
        return Response.redirect(location)

    @user(required=True)
    def delete(self, req):
        workers = Workers(self.ctx.db)
        worker = workers.find_id(req.ctx.args['id'])
        if worker is None:
            return Response.not_found()
        if not req.ctx.state['user'].can_write(worker.provider_id):
            return Response.forbidden()
        workers.remove_id(worker.id)
        location = WorkersListAdmin.route.url(req, id=worker.provider_id)
        return Response.redirect(location)


def block_workers(req, workers):
    return [{'worker': worker,
             'path': WorkerAdmin.route.path(id=worker.id)}
            for worker in workers]


class WorkersListAdmin(Resource):

    route = Route('/home/providers/{id}/workers/list', id=IdArg('id'))

    @xml('pages/providers-list-admin/html.xsl')
    @user(required=True)
    def get(self, req):
        found = Workers(self.ctx.db).find_provider(req.ctx.args['id'])
        return Response.ok({'workers': block_workers(req, found)})
