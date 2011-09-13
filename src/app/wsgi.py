from w3fu import config

from w3fu.web.base import Application
from w3fu.web.resources import Controller
from w3fu.storage.base import Storage

from app.collections.auth import Users
from app.collections.geo import Places
from app.resources.index import Index
from app.resources.test import PlanJson, PlanXml, TestHtml
from app.resources.auth import Login, Register
from app.resources.home import Home
from app.resources.geo import PlaceSuggest
#from w3fu.res.firms import FirmsPublic, FirmPublic, FirmsAdmin, FirmAdmin


controller = Controller([Index, Home,
                         Login, Register,
                         PlaceSuggest,
#                         FirmsPublic, FirmPublic, FirmsAdmin, FirmAdmin,
                         PlanJson, PlanXml, TestHtml])

storage = Storage([Users, Places])
app = Application(controller, storage)
