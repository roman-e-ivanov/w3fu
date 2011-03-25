import MySQLdb
from MySQLdb.cursors import DictCursor

from w3fu import config

from w3fu.web import Application
from w3fu.data.xml import XSLT
from w3fu.storage import Pool
from w3fu.storage.access import Database

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

conn_config = {
               'host': config.conn_host,
               'db': config.conn_db,
               'user': config.conn_user,
               'passwd': config.conn_passwd,
               'use_unicode': True,
               'charset': 'utf8'
               }

storage = Pool(lambda: Database(driver=MySQLdb, config=conn_config))
xslt = XSLT(config.xsl_path)
app = Application(controller, storage, xslt)
