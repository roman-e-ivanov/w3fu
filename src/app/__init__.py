from w3fu.http import Application
from w3fu.routing import Router

from app.routing import router
from app import resources


application = Application(router)
