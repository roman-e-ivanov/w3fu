class State(object):

    def __init__(self, req):
        self._req = req


class StateHandler(object):

    def __init__(self, **args):
        self._args = args

    def __call__(self, req):
        req.ctx.state = State(req)
