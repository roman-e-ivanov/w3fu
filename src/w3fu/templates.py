from json import load

OP_KEY = ''


class Template(object):

    @classmethod
    def load(cls, path):
        f = open(path, 'r')
        template = load(f)
        f.close()
        return cls(template)

    def __init__(self, template):
        self._body = template.get('body')
        inline = dict([(k, Template(v))
                           for k, v in template.get('inline', {}).iteritems()])
        include = dict([(k, Template.load(v))
                       for k, v in template.get('include', {}).iteritems()])
        self._subs = include
        self._subs.update(inline)

    def render(self, **ctx):
        return self(self._body, ctx)

    def __call__(self, op, ctx):
        if isinstance(op, dict):
            try:
                return getattr(self, op[OP_KEY])(op, ctx)
            except KeyError:
                return dict([(k, self(v, ctx)) for k, v in op.iteritems()])
        if isinstance(op, list):
            return [self(v, ctx) for v in op]
        return op

    def call(self, op, ctx):
        params = self(op.get('params', {}), ctx)
        return self._subs[op['name']].render(**dict(ctx, **params))

    def each(self, op, ctx):
        lst = self(op['list'], ctx)
        inner = self(op.get('inner', '.'), ctx)
        new_ctx = dict(ctx)
        for v in lst:
            new_ctx[inner] = v
            yield(self(op['block'], new_ctx))

    def join(self, op, ctx):
        lst = self(op['list'], ctx)
        separator = self(op.get('separator', ''), ctx)
        return separator.join([str(v) for v in lst])

    def data(self, op, ctx):
        path = self(op['path'], ctx)
        res = ctx
        for p in path:
            res = res[p]
        return res

    def ifelse(self, op, ctx):
        test = self(op['test'], ctx)
        return self(op.get('true' if test else 'false', ''), ctx)

    def format(self, op, ctx):
        text = self(op['text'], ctx)
        args = self(op['args'], ctx)
        return text.format(**args)


template = {
            'body': {
                     '': 'join',
                     'list': {
                              '': 'each',
                              'list': {'': 'data', 'path': ['root', 'x']},
                              'block': {
                                        '': 'join',
                                        'list': ['static', {'': 'data', 'path': ['.', 'y']}]
                                        }
                              }
                     }
            }

data = {
        'x': [{'y': 8}, {'y': 9}]
        }

t = Template(template)
print t.render(root=data)

from xml.etree.ElementTree import XMLParser, ElementTree

xml = '''
<root>
test1
<e1/>
test2
<e2/>
test3
<e3/>
test4
</root>
'''

class Builder(object):

    def close(self):
        print('close')

    def data(self, data):
        print('data = ' + str(data))

    def start(self, tag, attrs):
        print('start tag = ' + str(tag))

    def end(self, tag):
        print('end tag = ' + str(tag))



parser = XMLParser(target=Builder())
parser.feed(xml)
parser.close()

print('----------')

tree = ElementTree()
tree.parse("test.xml")
root = tree.getroot()
for e in root:
    print e.tag


template = '''
<template>
    <template name="t1"></template>
    <template name="t2" src="...">
</template>
'''


class Operation(object):

    def __init__(self, static, dynamic):
        self._static = static
        self._dynamic = dynamic
