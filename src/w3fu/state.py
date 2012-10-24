class State(object):

    def __init__(self, handler):
        self._handler = handler

    def __get__(self, ctx, owner):
        value = self._value(ctx)
        setattr(ctx, self._name, value)
        return value
