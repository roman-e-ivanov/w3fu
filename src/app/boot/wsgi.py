from w3fu.base import Application, Context
from w3fu.routing import Router
from w3fu.storage.base import Database
from w3fu.state import StateHandler

from app import config

from app.resources.debug import Debug
from app.resources.index import Index
from app.resources.home import Home
from app.resources.auth import Login, Register, ShortcutLogin
from app.resources.firms import FirmPublic, FirmsPublic, FirmAdmin, FirmsAdmin
from app.resources.geo import PlaceSuggest

from app.state import SessionState, UserState


resources = [Debug,
             Index, Home,
             ShortcutLogin, Login, Register,
             FirmPublic, FirmsPublic, FirmAdmin, FirmsAdmin,
             PlaceSuggest]

database = Database(config.db_uri, config.db_name)

ctx = Context(db=database)

router = Router([cls(ctx) for cls in resources])

state = StateHandler(router,
                     session_id=SessionState(),
                     user=UserState(ctx))

app = Application(ctx, state)
