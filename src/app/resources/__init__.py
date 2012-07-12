from w3fu.routing import Router
from w3fu.resources import BaseResource


class Resource(BaseResource):

    def _extra(self, data):
        data['user'] = self._ctx.state['user']

    def get(self, ctx):
        return self._ok({})


from app.resources import debug, test, index, home, auth, \
    providers, workers, services

resources = [debug.Debug, test.Test,
             index.Index, home.Home,
             auth.ShortcutLogin, auth.Login, auth.Register,
             providers.ProviderPublic,
             providers.ProvidersPublic,
             providers.ProviderAdmin,
             providers.ProvidersListAdmin,
             providers.ProvidersAdmin,
             workers.WorkerAdmin,
             workers.WorkersListAdmin,
             workers.WorkersAdmin,
             services.ServiceAdmin,
             services.ServicesAdmin,
             services.ServicesListAdmin]

router = Router(resources)
