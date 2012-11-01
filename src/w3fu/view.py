import sys
import os.path
import logging
import scss
import json
import shutil
from codecs import open

logging.getLogger('scss').addHandler(logging.StreamHandler())


class Blocks(object):

    def __init__(self, config):
        self.blocks_dir = config.blocks_dir
        self.static_dir = config.static_dir
        self._media_extensions = config.media_extensions
        self._static_formats = config.static_formats
        self._blocks = {}
        self._css_root_block = self[config.css_root_block]
        self._js_root_block = self[config.js_root_block]

    def __getitem__(self, rel_block_dir):
        try:
            return self._blocks[rel_block_dir]
        except KeyError:
            block = Block(self, rel_block_dir)
            self._blocks[rel_block_dir] = block
            return block

    def make_static(self):
        #shutil.rmtree(self.static_dir, ignore_errors=True)
        self._make_media()
        for fmt in self._static_formats:
            self._css_root_block.make_css(fmt)
            self._js_root_block.make_js(fmt)

    def _make_media(self):
        for src_dir, _, filenames in os.walk(self.blocks_dir):
            media = []
            for filename in filenames:
                ext = os.path.splitext(filename)[1]
                if ext in self._media_extensions:
                    media.append(filename)
            if not media:
                continue
            rel_dst_dir = os.path.relpath(src_dir, self.blocks_dir)
            dst_dir = os.path.join(self.static_dir, rel_dst_dir)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            for filename in media:
                src_path = os.path.join(src_dir, filename)
                dst_path = os.path.join(dst_dir, filename)
                shutil.copyfile(src_path, dst_path)


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

    def make_css(self, fmt):
        css_dir = os.path.join(self._blocks.static_dir, self._rel_block_dir)
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

    def make_js(self, fmt):
        included = set()
        def includer(writer, current):
            if current in included:
                return
            included.add(current)
            for block_dir in current.include_js:
                includer(writer, self._blocks[block_dir])
            writer.write(current.js(fmt))
        js_dir = os.path.join(self._blocks.static_dir, self._rel_block_dir)
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
                self._src = json.load(f)
        except IOError:
            print >> sys.stderr, "Error loading " + self.block_dir
            self._src = {}
