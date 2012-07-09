from w3fu import base, routing, state, view, storage

from app import config
from app.state import SessionState, UserState

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

view.Blocks.push(root_dir=config.blocks_root)
storage.Database.push(uri=config.db_uri, dbname=config.db_name)

ctx = base.Context()

router = routing.Router(ctx, resources)

state = state.StateHandler(router,
                           session_id=SessionState(),
                           user=UserState())

app = base.Application(ctx, state)
