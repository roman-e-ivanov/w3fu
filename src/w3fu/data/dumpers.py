from lxml import etree
from json import dumps
from time import mktime

from w3fu.data.codecs import b64e


class Dumper(object):

    def __init__(self, format):
        self._format = format

    def _default(self, data):
        try:
            return b64e(data.binary)
        except AttributeError:
            pass
        try:
            return int(mktime(data.timetuple()))
        except AttributeError:
            pass
        return str(data)


class JsonDumper(Dumper):

    def dump(self, data):
        return dumps(data, indent=4, ensure_ascii=False, default=self._default)

    def _default(self, data):
        try:
            return data.dump(format)
        except AttributeError:
            pass
        return super(JsonDumper, self)._default(data)


class XmlDumper(Dumper):

    def __init__(self, format, xslt=None):
        super(XmlDumper, self).__init__(format)
        self._xslt = None
        if xslt is not None:
            self._xslt = etree.XSLT(etree.parse(xslt))
        self._format = format

    def dump(self, data, name, no_xslt=False):
        e = self._element(name, data)
        if self._xslt is not None and not no_xslt:
            e = self._xslt(e)
        return etree.tostring(e, pretty_print=True, encoding='UTF-8')

    def _element(self, name, data):
        def worker(root, name, data, extend=True):
            name = name.replace('_', '-')
            if data is None:
                return
            if hasattr(data, 'dump'):
                worker(root, name, data.dump(self._format), extend)
                return
            if isinstance(data, basestring):
                if extend:
                    etree.SubElement(root, name).text = data
                else:
                    root.set(name, data)
                return
            if isinstance(data, dict):
                e = etree.SubElement(root, name)
                for k, v in data.iteritems():
                    worker(e, k, v, False)
                return
            if isinstance(data, (list, tuple)):
                e = etree.SubElement(root, name)
                for v in data:
                    worker(e, 'i', v)
                return
            s = self._default(data)
            if extend:
                etree.SubElement(root, name).text = s
            else:
                root.set(name, s)
        e = etree.Element(name)
        for k, v in data.iteritems():
            worker(e, k, v)
        return e
