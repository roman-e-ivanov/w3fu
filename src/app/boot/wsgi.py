from w3fu.http import Context, Application
from w3fu.routing import Router
from w3fu.state import StateHandler
from w3fu.storage import Database
from w3fu.view import Blocks

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

Blocks.push(root_dir=config.blocks_root)
Database.push(uri=config.db_uri, dbname=config.db_name)

ctx = Context()

router = Router(ctx, resources)

state = StateHandler(router,
                     session_id=SessionState(),
                     user=UserState())

app = Application(ctx, state)
