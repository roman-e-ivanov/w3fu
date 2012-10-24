from w3fu.http import BaseRequest, Application

from app.resources import router
from app.state import UserState, SessionIdState


class Request(BaseRequest):

    user = UserState()
    session_id = SessionIdState()


application = Application(router, Request)
