import os.path
from json import load
from codecs import open


class Blocks(object):

    def __init__(self, root_dir):
        self._root_dir = root_dir
        self._blocks = {}

    def __getitem__(self, block_dir):
        try:
            return self._blocks[block_dir]
        except KeyError:
            block = Block(self, os.path.join(self._root_dir, block_dir))
            self._blocks[block_dir] = block
            return block


class Operand(object):

    def __init__(self, block, src):
        self._data = src

    def render(self, ctx):
        return self._data


class ListOperand(object):

    def __init__(self, block, src):
        self._ops = [block.compile(v) for v in src]

    def render(self, ctx):
        return [op.render(ctx) for op in self._ops]


class DictOperand(object):

    def __init__(self, block, src):
        self._ops = dict([(k, block.compile(v)) for k, v in src.iteritems()])

    def render(self, ctx):
        return dict([(k, op.render(ctx)) for k, op in self._ops.iteritems()])


class Function(object):

    _required = {}

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    def __init__(self, block, src):
        self._block = block
        self._data = block.compile(src[self.name()])
        self._args = {}
        for name, default in self._required.iteritems():
            try:
                value = src[name]
            except KeyError:
                if default is None:
                    raise Exception('Parameter required', name)
                value = default
            self._args[name] = block.compile(value)


class Join(Function):

    _required = {'separator': ''}

    def render(self, ctx):
        separator = self._args['separator'].render(ctx)
        return separator.join([str(v) for v in self._data.render(ctx)])


class Map(Function):

    _required = {'list': None, 'local': '_'}

    def render(self, ctx):
        local = self._args['local'].render(ctx)
        new_ctx = dict(ctx)
        for v in self._args['list'].render(ctx):
            new_ctx[local] = v
            yield(self._data.render(new_ctx))


class If(Function):

    _required = {'true': '', 'false': ''}

    def render(self, ctx):
        test = self._data.render(ctx)
        result = self._args['true'] if test else self._args['false']
        return result.render(ctx)


class Data(Function):

    _required = {'default': ''}

    def render(self, ctx):
        path = self._data.render(ctx)
        res = ctx
        for p in path:
            try:
                res = res[p]
            except KeyError:
                return self._args['default'].render(ctx)
        return res


class Fill(Function):

    _required = {'args': {}}

    def render(self, ctx):
        ext = self._args['args'].render(ctx)
        return self._data.render(ctx).format(**dict(ctx, **ext))


class Call(Function):

    _required = {'args': {}}

    def render(self, ctx):
        ext = self._args['args'].render(ctx)
        sub = self._block.subs[self._data.render(ctx)]
        return sub.render(dict(ctx, **ext))


class File(Function):

    def __init__(self, block, src):
        super(File, self).__init__(block, src)
        self._load()

    def _load(self):
        path = os.path.join(self._block.work_dir, self._data.render({}))
        f = open(path, 'r', 'utf-8')
        self._content = f.read()
        f.close()

    def render(self, ctx):
        return self._content


class Block(object):

    _functions = [Join, Map, If, Data, Fill, Call, File]

    _functions_by_name = dict([(op.name(), op) for op in _functions])

    def __init__(self, blocks, work_dir):
        self.work_dir = work_dir
        self._load()
        include = self._src.get('include', {})
        define = self._src.get('define', {})
        self.subs = dict([(k, blocks[v]) for k, v in include.iteritems()])
        self.subs.update(dict([(k, self.compile(v))
                               for k, v in define.iteritems()]))
        self._body = self.compile(self._src.get('body'))

    def compile(self, src):
        if isinstance(src, dict):
            for k in src.keys():
                cls = self._functions_by_name.get(k)
                if cls:
                    return cls(self, src)
            return DictOperand(self, src)
        if isinstance(src, list):
            return ListOperand(self, src)
        return Operand(self, src)

    def render(self, ctx):
        return self._body.render(ctx)

    def _load(self):
        path = os.path.join(self.work_dir, 'block.json')
        f = open(path, 'r')
        self._src = load(f)
        f.close()
