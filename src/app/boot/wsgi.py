from w3fu.base import Application, Context
from w3fu.routing import Router
from w3fu.storage.base import Database

from app import config

from app.resources.index import Index
from app.resources.auth import Login, Register
from app.resources.home import Home
from app.resources.geo import PlaceSuggest


resources = [Index, Home, Login, Register, PlaceSuggest]

database = Database(config.db_uri, config.db_name)

ctx = Context(db=database)

handler = Router([cls(ctx) for cls in resources])

app = Application(ctx, handler)
