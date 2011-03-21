from lxml import etree


def element(name, data):
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
