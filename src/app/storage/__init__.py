from w3fu.storage.base import Storage

from app import config
from app.storage.collections import collections


storage = Storage(config.db_uri, config.db_name, collections)
