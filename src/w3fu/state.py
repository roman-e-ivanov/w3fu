class State(object):

    def __init__(self, ctx, args):
        self._ctx = ctx
        self._args = args
        self._get = {}
        self._set = {}
        self._del = set()

    def __getitem__(self, key):
        try:
            return self._get[key]
        except KeyError:
            if key not in self._args:
                raise AttributeError
            self._get[key] = self._args[key].get(self._ctx)
            return self._get[key]

    def __setitem__(self, key, value):
        self._set[key] = value

    def __delitem__(self, key):
        self._del.add(key)

    def output(self, resp):
        for name, value in self._set.iteritems():
            self._args[name].set(self._ctx, resp, value)
        for name in self._del:
            self._args[name].delete(self._ctx, resp)


class StateHandler(object):

    def __init__(self, **args):
        self._args = args

    def __call__(self, ctx):
        ctx.state = State(ctx, self._args)
        resp = self.next(ctx)
        ctx.state.output(resp)
        return resp
