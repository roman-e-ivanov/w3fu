from w3fu.base import Response
from w3fu.routing import Route
from w3fu.data.args import StrArg, IdArg
from w3fu.resources import Form, Resource

from app.resources.middleware.context import user
from app.resources.middleware.transform import xml

from app.storage import providers, workers


def block_worker(doc):
    nav = {'main': WorkerAdmin.route.path(id=doc.id)}
    return {'doc': doc, 'nav': nav}


class WorkerForm(Form):

    name = StrArg('name', min_size=1, max_size=100)


class WorkersAdmin(Resource):

    route = Route('/home/providers/{id}/workers', id=IdArg('id'))

    @xml('pages/workers-admin/html.xsl')
    @user(required=True)
    def get(self, ctx):
        return Response.ok({})

    @xml('pages/workers-admin/html.xsl')
    @user(required=True)
    def post(self, ctx):
        provider_id = ctx.args['id']
        provider = providers.Provider.find_id(provider_id)
        if provider is None:
            return Response.not_found()
        if not ctx.state['user'].can_write(provider_id):
            return Response.forbidden()
        form = WorkerForm(ctx.req)
        if form.errors:
            return Response.ok({'form': form})
        worker = workers.Worker.new(provider_id, form.data['name'])
        workers.Worker.insert(worker)
        return Response.redirect(WorkerAdmin.route.url(ctx.req, id=worker.id))


class WorkerAdmin(Resource):

    route = Route('/home/workers/{id}', id=IdArg('id'))

    @xml('pages/worker-admin/html.xsl')
    @user(required=True)
    def get(self, ctx):
        worker = workers.Worker.find_id(ctx.args['id'])
        if worker is None:
            return Response.not_found()
        return Response.ok({'worker': worker})

    @xml('pages/worker-admin/html.xsl')
    @user(required=True)
    def put(self, ctx):
        worker = workers.Worker.find_id(ctx.args['id'])
        if worker is None:
            return Response.not_found()
        if not ctx.state['user'].can_write(worker.provider_id):
            return Response.forbidden()
        form = WorkerForm(ctx.req)
        if form.errors:
            return Response.ok({'form': form})
        worker.name = form.data['name']
        workers.Worker.update(worker)
        location = WorkersListAdmin.route.url(ctx.req, id=worker.provider_id)
        return Response.redirect(location)

    @user(required=True)
    def delete(self, ctx):
        worker = workers.Worker.find_id(ctx.args['id'])
        if worker is None:
            return Response.not_found()
        if not ctx.state['user'].can_write(worker.provider_id):
            return Response.forbidden()
        workers.Worker.remove_id(worker.id)
        location = WorkersListAdmin.route.url(ctx.req, id=worker.provider_id)
        return Response.redirect(location)


class WorkersListAdmin(Resource):

    route = Route('/home/providers/{id}/workers/list', id=IdArg('id'))

    @xml('pages/workers-list-admin/html.xsl')
    @user(required=True)
    def get(self, ctx):
        found = workers.Worker.find_provider(ctx.args['id'])
        return Response.ok({'workers': [block_worker(doc)
                                        for doc in found]})
