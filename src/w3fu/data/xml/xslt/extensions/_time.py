from time import time as _time, gmtime as _gmtime


def time(_):
    return _time()

def gmtime(_, index, secs=None):
    return _gmtime(secs)[index]
