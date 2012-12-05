from w3fu.http import Application
from w3fu.routing import Router

from app.http import Request
from app.routing import router
from app import resources


application = Application(router, Request)
