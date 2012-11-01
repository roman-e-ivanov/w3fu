import sys
import os.path
import logging
import scss
from json import load
from codecs import open


logging.getLogger('scss').addHandler(logging.StreamHandler())


class Blocks(object):

    def __init__(self, blocks_dir):
        self.blocks_dir = blocks_dir
        self._blocks = {}

    def __getitem__(self, rel_block_dir):
        try:
            return self._blocks[rel_block_dir]
        except KeyError:
            block = Block(self, rel_block_dir)
            self._blocks[rel_block_dir] = block
            return block


class Operand(object):

    def __init__(self, block, src):
        self._data = src

    def render(self, fmt, ctx):
        return self._data


class ListOperand(object):

    def __init__(self, block, src):
        self._ops = [block.compile(v) for v in src]

    def render(self, fmt, ctx):
        return [op.render(fmt, ctx) for op in self._ops]


class DictOperand(object):

    def __init__(self, block, src):
        self._ops = dict([(k, block.compile(v)) for k, v in src.iteritems()])

    def render(self, fmt, ctx):
        return dict([(k, op.render(fmt, ctx))
                     for k, op in self._ops.iteritems()])


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

    def render(self, fmt, ctx):
        separator = self._args['separator'].render(fmt, ctx)
        return separator.join([str(v) for v in self._data.render(fmt, ctx)])


class Map(Function):

    _required = {'list': None, 'local': '_'}

    def render(self, fmt, ctx):
        local = self._args['local'].render(fmt, ctx)
        new_ctx = dict(ctx)
        for v in self._args['list'].render(fmt, ctx):
            new_ctx[local] = v
            yield(self._data.render(fmt, new_ctx))


class If(Function):

    _required = {'true': '', 'false': ''}

    def render(self, fmt, ctx):
        test = self._data.render(fmt, ctx)
        result = self._args['true'] if test else self._args['false']
        return result.render(fmt, ctx)


class Data(Function):

    _required = {'default': ''}

    def render(self, fmt, ctx):
        path = self._data.render(fmt, ctx)
        res = ctx
        for p in path:
            try:
                res = res[p]
            except KeyError:
                return self._args['default'].render(fmt, ctx)
        return res


class Fill(Function):

    _required = {'args': {}}

    def render(self, fmt, ctx):
        ext = self._args['args'].render(fmt, ctx)
        return self._data.render(fmt, ctx).format(**dict(ctx, **ext))


class Call(Function):

    _required = {'args': {}}

    def render(self, fmt, ctx):
        ext = self._args['args'].render(fmt, ctx)
        sub = self._block.subs[self._data.render(fmt, ctx)]
        return sub.render(fmt, dict(ctx, **ext))


class File(Function):

    def __init__(self, block, src):
        super(File, self).__init__(block, src)
        self._load()

    def _load(self):
        path = os.path.join(self._block.block_dir, self._data.render(None, {}))
        with open(path, 'r', 'utf-8') as f:
            self._content = f.read()

    def render(self, fmt, ctx):
        return self._content


class Block(object):

    _functions = [Join, Map, If, Data, Fill, Call, File]

    _functions_by_name = dict([(op.name(), op) for op in _functions])

    def __init__(self, blocks, rel_block_dir):
        self._blocks = blocks
        self._rel_block_dir = rel_block_dir
        self.block_dir = os.path.join(blocks.blocks_dir, rel_block_dir)
        self._load()
        self.include_js = self._src.get('include_js', [])
        include = self._src.get('include', {})
        define = self._src.get('define', {})
        self.subs = dict([(k, blocks[v])
                          for k, v in include.iteritems()])
        self.subs.update(dict([(k, self.compile(v))
                               for k, v in define.iteritems()]))
        self._body = {}
        for fmt, body in self._src.get('body', {}).iteritems():
            self._body[fmt] = self.compile(body)

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

    def render(self, fmt, ctx):
        body = self._body.get(fmt) or self._body.get('all')
        if body is None:
            return ''
        return body.render(fmt, ctx)

    def make_css(self, fmt, static_dir):
        css_dir = os.path.join(static_dir, self._rel_block_dir)
        css_path = os.path.join(css_dir, fmt + '.css')
        scss_path = os.path.join(self.block_dir, fmt + '.scss')
        scss.LOAD_PATHS = self._blocks.blocks_dir
        with open(scss_path, 'r') as f:
            scss_string = f.read()
        compiler = scss.Scss()
        css = compiler.compile(scss_string)
        if not os.path.exists(css_dir):
            os.makedirs(css_dir)
        with open(css_path, 'w') as f:
            f.write(css)

    def make_js(self, fmt, static_dir):
        included = set()
        def includer(writer, current):
            if current in included:
                return
            included.add(current)
            for block_dir in current.include_js:
                includer(writer, self._blocks[block_dir])
            writer.write(current.js(fmt))
        js_dir = os.path.join(static_dir, self._rel_block_dir)
        js_path = os.path.join(js_dir, fmt + '.js')
        if not os.path.exists(js_dir):
            os.makedirs(js_dir)
        with open(js_path, 'w') as f:
            includer(f, self)

    def js(self, fmt):
        scripts = ''
        for name in ['common', fmt]:
            js_path = os.path.join(self.block_dir, name + '.js')
            try:
                with open(js_path, 'r') as f:
                    script = f.read()
            except IOError:
                continue
            scripts += '// ' + js_path + '\n'
            scripts += script + '\n'
        return scripts

    def _load(self):
        path = os.path.join(self.block_dir, 'block.json')
        try:
            with open(path, 'r') as f:
                self._src = load(f)
        except IOError:
            print >> sys.stderr, "Error loading " + self.block_dir
            self._src = {}
