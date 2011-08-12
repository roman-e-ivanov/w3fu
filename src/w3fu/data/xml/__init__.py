from lxml import etree
from time import mktime


def element(name, data):
    def worker(root, name, data, extend=True):
        name = name.replace('_', '-')
        if isinstance(data, basestring):
            if extend:
                etree.SubElement(root, name).text = data
            else:
                root.set(name, data)
            return
        try:
            i = data.iteritems()
            e = etree.SubElement(root, name)
            for k, v in i:
                worker(e, k, v, False)
            return
        except AttributeError:
            pass
        try:
            for v in data:
                worker(root, name, v)
            return
        except TypeError:
            pass
        if extend:
            etree.SubElement(root, name).text = str(data)
        else:
            root.set(name, str(data))
    e = etree.Element(name)
    for k, v in data.iteritems():
        worker(e, k, v)
    return e
