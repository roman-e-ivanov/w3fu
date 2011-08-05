from w3fu import config

from w3fu.web import Application

from w3fu.data.xml.xslt import XSLT
from w3fu.data.xml.xslt.extensions import _time

from w3fu.storage import Database
from w3fu.storage.collections.auth import Users

from w3fu.res import Controller
from w3fu.res.index import Index
from w3fu.res.test import PlanJson, PlanXml, TestHtml
from w3fu.res.auth import Login, Register
from w3fu.res.home import Home
#from w3fu.res.firms import FirmsPublic, FirmPublic, FirmsAdmin, FirmAdmin


controller = Controller([Index, Home,
                         Login, Register,
#                         FirmsPublic, FirmPublic, FirmsAdmin, FirmAdmin,
                         PlanJson, PlanXml, TestHtml])

xslt = XSLT({'time': _time})
db = Database([Users])
app = Application(controller, db, xslt)
