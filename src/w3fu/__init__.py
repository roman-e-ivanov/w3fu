import MySQLdb

from w3fu import config

from w3fu.web import Application

from w3fu.data.xml.xslt import XSLT
from w3fu.data.xml.xslt.extensions import _time

from w3fu.storage import Storage
from w3fu.storage.mysql import Database

from w3fu.res import Controller
from w3fu.res.index import Index
from w3fu.res.test import PlanJson, PlanXml, TestHtml
from w3fu.res.auth import Login, Register
from w3fu.res._openid import OpenIdAuth
from w3fu.res.home import Home


controller = Controller([Index, Home,
                         PlanJson, PlanXml, TestHtml,
                         Login,
                         Register,
                         OpenIdAuth])

xslt = XSLT(config.xsl_path, {
                              'time': _time,
                              })

storage = Storage(Database)

app = Application(controller, storage, xslt)
