from w3fu.routing import Router

from app.resources import test, auth
#debug, index, home, providers, workers, services

resources = [test.Test(), auth.ShortcutLogin(), auth.Login(), auth.Register(),
#             debug.Debug(),
#             index.Index, home.Home,
#             providers.ProviderPublic,
#             providers.ProvidersPublic,
#             providers.ProviderAdmin,
#             providers.ProvidersListAdmin,
#             providers.ProvidersAdmin,
#             workers.WorkerAdmin,
#             workers.WorkersListAdmin,
#             workers.WorkersAdmin,
#             services.ServiceAdmin,
#             services.ServicesAdmin,
#             services.ServicesListAdmin
    ]

router = Router(resources)
