from w3fu import config

from w3fu.web.base import Application
from w3fu.web.resources import Controller

from w3fu.storage import Storage
from w3fu.storage.collections.auth import Users
from w3fu.storage.collections.geo import Places

from w3fu.resources.index import Index
from w3fu.resources.test import PlanJson, PlanXml, TestHtml
from w3fu.resources.auth import Login, Register
from w3fu.resources.home import Home
from w3fu.resources.geo import PlaceSuggest
#from w3fu.res.firms import FirmsPublic, FirmPublic, FirmsAdmin, FirmAdmin


controller = Controller([Index, Home,
                         Login, Register,
                         PlaceSuggest,
#                         FirmsPublic, FirmPublic, FirmsAdmin, FirmAdmin,
                         PlanJson, PlanXml, TestHtml])

storage = Storage([Users, Places])
app = Application(controller, storage)
