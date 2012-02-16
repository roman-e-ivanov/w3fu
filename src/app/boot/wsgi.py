from w3fu.base import Application, Context
from w3fu.routing import Router

from app.storage import storage
from app.resources import resources


ctx = Context(storage=storage)
router = Router([cls(ctx) for cls in resources])
app = Application(ctx, router)
