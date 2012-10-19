from w3fu.http import Application

from app.state import state
from app.resources import router


state.next = router

application = Application(state)
