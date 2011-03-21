from time import time as _time, gmtime as _gmtime


def time(_):
    return _time()

def gmtime(_, secs=None, index=0):
    return _gmtime(secs)[index]
