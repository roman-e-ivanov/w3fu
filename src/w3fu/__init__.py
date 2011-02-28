import MySQLdb
from MySQLdb.cursors import DictCursor

from w3fu import config

from w3fu.web import Application
from w3fu.data.xml import XSLT
from w3fu.storage import Storage
from w3fu.storage.dbapi import Connection
from w3fu.storage.orm.auth import Users, Sessions
from w3fu.storage.orm._openid import OpenIdStore

from w3fu.res import Controller
from w3fu.res.index import Index
from w3fu.res.test import PlanJson, TestHtml
from w3fu.res.auth import Login, Register
from w3fu.res._openid import OpenIdAuth


controller = Controller([Index,
                         PlanJson, TestHtml,
                         Login,
                         Register,
                         OpenIdAuth])

conn_config = {
               'host': config.conn_host,
               'db': config.conn_db,
               'user': config.conn_user,
               'passwd': config.conn_passwd,
               'cursorclass': DictCursor,
               'use_unicode': True,
               'charset': 'utf8'
               }

storage = Storage(lambda storage: Connection(
                                             storage=storage,
                                             driver=MySQLdb,
                                             config=conn_config,
                                             mappers=(Users,
                                                      Sessions,
                                                      OpenIdStore)))

xslt = XSLT(config.xsl_path)

app = Application(controller, storage, xslt)
