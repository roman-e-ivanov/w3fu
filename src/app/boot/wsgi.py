from w3fu.base import Application, Context
from w3fu.routing import Router
from w3fu.storage.base import Database
from w3fu.state import StateHandler
from w3fu.templating import Blocks

from app import config

from app.resources.debug import Debug
from app.resources.test import Test
from app.resources.index import Index
from app.resources.home import Home
from app.resources.auth import Login, Register, ShortcutLogin
from app.resources.providers import ProviderPublic, ProvidersPublic, \
    ProviderAdmin, ProvidersAdmin, ProvidersListAdmin
from app.resources.workers import WorkerAdmin, WorkersAdmin, WorkersListAdmin
from app.resources.services import ServiceAdmin, ServicesAdmin, \
    ServicesListAdmin
from app.resources.geo import PlaceSuggest

from app.state import SessionState, UserState
from app.caching import CacheHandler


resources = [Debug, Test,
             Index, Home,
             ShortcutLogin, Login, Register,
             ProviderPublic, ProvidersPublic,
             ProviderAdmin, ProvidersListAdmin, ProvidersAdmin,
             WorkerAdmin, WorkersListAdmin, WorkersAdmin,
             ServiceAdmin, ServicesAdmin, ServicesListAdmin,
             PlaceSuggest]

database = Database(config.db_uri, config.db_name)
blocks = Blocks(config.blocks_root)

ctx = Context(db=database, blocks=blocks)

router = Router([cls(ctx) for cls in resources])

state = StateHandler(router,
                     session_id=SessionState(),
                     user=UserState(ctx))

cache = CacheHandler(state)

app = Application(ctx, cache)
