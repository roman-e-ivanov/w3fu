import os
from lxml import etree

from w3fu import config


class XSLT(object):

    def __init__(self, root, extensions):
        for name, extension in extensions.iteritems():
            ns = etree.FunctionNamespace(config.xslt_ext_prefix + name)
            ns.prefix = name
            for func in dir(extension):
                if func[0] == '_':
                    continue
                ns[func] = getattr(extension, func)
        self._templates = {}
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if not os.path.isfile(path):
                continue
            name, ext = os.path.splitext(name)
            if ext == '.xsl':
                self._templates[name] = etree.XSLT(etree.parse(path))

    def transform(self, element, template=None):
        e = element if template is None else self._templates[template](element)
        return etree.tostring(e, pretty_print=True, encoding='UTF-8')
