from w3fu.storage.base import Storage

from app import config
from app.storage.collections import collections


storage = Storage(config.db_host, config.db_port, config.db_name, collections)
