from w3fu.util import class_wrapper

from app.state import UserState


@class_wrapper(UserState())
class User(object):

    def __call__(self, req):
        return {'user': req.user}


class Form(object):

    def __call__(self, req):
        try:
            return {'form': req.form}
        except AttributeError:
            return {}


public_mixins = [Form(), User()]
