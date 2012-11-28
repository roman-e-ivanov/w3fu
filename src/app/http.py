from w3fu.http import BaseRequest

from app.state import UserState


class Request(BaseRequest):

    user = UserState('user')
