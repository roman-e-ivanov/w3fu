from w3fu.base import Application, Context
from w3fu.routing import Router
from w3fu.storage.base import Storage

from app import config

from app.resources.index import Index
from app.resources.auth import Login, Register
from app.resources.home import Home
from app.resources.geo import PlaceSuggest

from app.storage.collections.auth import Users
from app.storage.collections.geo import Places


collections = [Users, Places]
resources = [Index, Home, Login, Register, PlaceSuggest]

storage = Storage(config.db_uri, config.db_name, collections)

ctx = Context(storage=storage)

handler = Router([cls(ctx) for cls in resources])

app = Application(ctx, handler)
