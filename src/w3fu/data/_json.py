from json import dumps
from time import mktime

from w3fu.data.util import b64e


def to_json(data, format):
    def default(obj):
        try:
            return obj.dump(format)
        except AttributeError:
            pass
        try:
            return b64e(obj.binary)
        except AttributeError:
            pass
        try:
            return int(mktime(obj.timetuple()))
        except AttributeError:
            raise TypeError
    return dumps(data, indent=4, ensure_ascii=False, default=default)
