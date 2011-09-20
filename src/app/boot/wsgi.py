from w3fu.web.base import Application
from w3fu.web.resources import Controller

from app.storage import storage
from app.resources import resources


app = Application(Controller(resources), storage)
