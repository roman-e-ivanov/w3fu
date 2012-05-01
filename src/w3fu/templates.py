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

    def render(self, ro, rw=None):
        return self(self._body, ro, rw or {})

    def __call__(self, op, ro, rw):
        if isinstance(op, dict):
            try:
                return getattr(self, op[OP_KEY])(op, ro, rw)
            except KeyError:
                return dict([(k, self(v, ro, rw)) for k, v in op.iteritems()])
        if isinstance(op, list):
            return [self(v, ro, rw) for v in op]
        return op

    def call(self, op, ro, rw):
        params = self(op.get('params', {}), ro, rw)
        return self._subs[op['name']].render(ro, dict(params))

    def join(self, op, ro, rw):
        seq = self(op['list'], ro, rw)
        return ''.join([str(v) for v in seq])

    def each(self, op, ro, rw):
        seq = self(op['list'], ro, rw)
        return [self(op['block'], v, rw) for v in seq]

    def ro(self, op, ro, rw):
        path = self(op.get('path', []), ro, rw)
        res = ro
        for p in path:
            res = res[p]
        return res

    def rw(self, op, ro, rw):
        path = self(op.get('name', []), ro, rw)
        res = ro
        for p in path:
            res = res[p]
        return res

    def ifelse(self, op, ro, rw):
        cond = self(op['test'], ro, rw)
        return self(op.get('true' if cond else 'false', ''), ro, rw)


template = {
            'body': {
                     '': 'join',
                     'list': {
                              '': 'each',
                              'list': {'': 'ro', 'path': 'x'},
                              'block': {
                                        '': 'join',
                                        'list': ['static', {'': 'ro', 'path': 'y'}]
                                        }
                              }
                     }
            }

data = {
        'x': [{'y': 8}, {'y': 9}]
        }

t = Template(template)
print t.render(data)
