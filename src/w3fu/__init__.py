import MySQLdb

from w3fu import config

from w3fu.web import Application
from w3fu.data.xml import XSLT
from w3fu.storage import Storage
from w3fu.storage.mysql import Database

from w3fu.res import Controller
from w3fu.res.index import Index
from w3fu.res.test import PlanJson, PlanXml, TestHtml
from w3fu.res.auth import Login, Register
from w3fu.res._openid import OpenIdAuth


controller = Controller([Index,
                         PlanJson, PlanXml, TestHtml,
                         Login,
                         Register,
                         OpenIdAuth])

storage = Storage(Database)
xslt = XSLT(config.xsl_path)
app = Application(controller, storage, xslt)
