from w3fu.http import Application
from w3fu.routing import Router

from app.http import Request

from app.resources.test import Test
from app.resources.index import Index
from app.resources.home import Home
from app.resources.auth import ShortcutLogin, Login, Register


resources = [Test(),
             Index(), Home(),
             ShortcutLogin(), Login(), Register()]

application = Application(Router(resources), Request)
