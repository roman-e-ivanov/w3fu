import os
from lxml import etree


def element(data, name):
    def worker(root, name, data):
        if isinstance(data, basestring):
            etree.SubElement(root, name).text = data
            return
        try:
            i = data.iteritems()
            e = etree.SubElement(root, name)
            for k, v in i:
                worker(e, k, v)
            return
        except AttributeError:
            pass
        try:
            for v in data:
                worker(root, name, v)
            return
        except TypeError:
            pass
        etree.SubElement(root, name).text = str(data)
    e = etree.Element(name)
    for k, v in data.iteritems():
        worker(e, k, v)
    return e


class XSLT(object):

    def __init__(self, root):
        self._templates = {}
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if not os.path.isfile(path):
                continue
            name, ext = os.path.splitext(name)
            if ext == '.xsl':
                self._templates[name] = etree.XSLT(etree.parse(path))

    def transform(self, name, data, template=None):
        e = element(data, name)
        if template is not None:
            e = self._templates[template](e)
        return etree.tostring(e, pretty_print=True, encoding='UTF-8')
