from w3fu.http import Context, Application

from app.state import state
from app.resources import router


state.next = router

application = Application(Context(), state)
