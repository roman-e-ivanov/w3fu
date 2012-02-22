from datetime import timedelta

from w3fu.cookies import Cookie
from w3fu.data.args import StrArg


class AuthCookie(Cookie):

    session_id = StrArg('u', ttl=timedelta(days=1))
