from w3fu.web.base import Application, Context
from w3fu.web.resources import Controller

from app.storage import storage
from app.resources import resources


ctx = Context(storage=storage)
app = Application(ctx, Controller(ctx, [cls(ctx) for cls in resources]))
