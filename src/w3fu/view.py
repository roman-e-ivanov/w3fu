import sys
import os.path
import logging
import scss
import json
import shutil
from codecs import open

logging.getLogger('scss').addHandler(logging.StreamHandler())


class View(object):

    def __init__(self, config):
        self.blocks_dir = config.blocks_dir
        self.static_dir = config.static_dir
        self._static_formats = config.static_formats
        self._root_block = config.root_block
        self._blocks = {}

    def __getitem__(self, block_name):
        try:
            return self._blocks[block_name]
        except KeyError:
            block = Block(self, block_name)
            self._blocks[block_name] = block
            return block

    def make_static(self):
        shutil.rmtree(self.static_dir, ignore_errors=True)
        blocks = self[self._root_block].tree()
        for block in blocks:
            block.make_static_copy()
            for fmt in self._static_formats:
                block.make_css(fmt)
                block.make_js(fmt)


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
        return separator.join([unicode(v)
                               for v in self._data.render(fmt, ctx)])


class Map(Function):

    _required = {'list': None, 'item': '_', 'index': '#'}

    def render(self, fmt, ctx):
        item_param = self._args['item'].render(fmt, ctx)
        index_param = self._args['index'].render(fmt, ctx)
        new_ctx = dict(ctx)
        for index, item in enumerate(self._args['list'].render(fmt, ctx)):
            new_ctx[index_param] = index
            new_ctx[item_param] = item
            yield(self._data.render(fmt, new_ctx))


class If(Function):

    _required = {'true': '', 'false': ''}

    def render(self, fmt, ctx):
        test = self._data.render(fmt, ctx)
        result = self._args['true'] if test else self._args['false']
        return result.render(fmt, ctx)


class Data(Function):

    _required = {'default': '', 'ctx': ''}

    def render(self, fmt, ctx):
        path = self._data.render(fmt, ctx)
        local_ctx = self._args['ctx'].render(fmt, ctx)
        result = local_ctx or ctx
        for p in path:
            try:
                result = result[p]
            except KeyError:
                return self._args['default'].render(fmt, ctx)
        return result


class Apply(Function):

    _required = {'args': {}}

    def render(self, fmt, ctx):
        args = self._args['args'].render(fmt, ctx)
        return self._data.render(fmt, dict(ctx, **args))


class Fill(Function):

    _required = {'args': {}}

    def render(self, fmt, ctx):
        args = self._args['args'].render(fmt, ctx)
        return self._data.render(fmt, ctx).format(**dict(ctx, **args))


class Call(Function):

    _required = {'args': {}}

    def render(self, fmt, ctx):
        ext = self._args['args'].render(fmt, ctx)
        sub = self._block.callables[self._data.render(fmt, ctx)]
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

    _functions = [Join, Map, If, Data, Apply, Fill, Call, File]

    _functions_by_name = dict([(op.name(), op) for op in _functions])

    def __init__(self, view, name):
        self._view = view
        self.name = name
        self.block_dir = os.path.join(view.blocks_dir, name)
        self._load()
        includes = self._src.get('include', [])
        self.includes = [view[block_name] for block_name in includes]
        self.callables = dict([(block.name, block) for block in self.includes])
        define = self._src.get('define', {})
        self.callables.update(dict([(sub_name, self.compile(sub))
                               for sub_name, sub in define.iteritems()]))
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

    def tree(self, current=None, collected=None, included=None):
        if current is None:
            current = self
        if included is None:
            included = set()
        if current in included:
            return collected
        if collected is None:
            collected = []
        included.add(current)
        for include in current.includes:
            self.tree(include, collected, included)
        collected.append(current)
        return collected

    def make_static_copy(self):
        src_dir = os.path.join(self.block_dir, 'static')
        if not os.path.exists(src_dir):
            return
        dst_dir = os.path.join(self._view.static_dir, self.name)
        shutil.copytree(src_dir, dst_dir)

    def make_css(self, fmt):
        if not self._src.get('css', False):
            return
        css_dir = os.path.join(self._view.static_dir, self.name)
        css_path = os.path.join(css_dir, fmt + '.css')
        if not os.path.exists(css_dir):
            os.makedirs(css_dir)
        with open(css_path, 'w') as f:
            tree = self.tree()
            for block in tree:
                css = block.css(fmt)
                if css:
                    f.write(css)

    def make_js(self, fmt):
        if not self._src.get('js', False):
            return
        js_dir = os.path.join(self._view.static_dir, self.name)
        js_path = os.path.join(js_dir, fmt + '.js')
        if not os.path.exists(js_dir):
            os.makedirs(js_dir)
        with open(js_path, 'w') as f:
            tree = self.tree()
            for block in tree:
                js = block.js(fmt)
                if js:
                    f.write(js)

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

    def css(self, fmt):
        compiler = scss.Scss(scss_opts={'compress': False})
        scss.LOAD_PATHS = self.block_dir
        for name in [fmt, 'all']:
            scss_path = os.path.join(self.block_dir, name + '.scss')
            try:
                with open(scss_path, 'r') as f:
                    scss_src = f.read()
                css = compiler.compile(scss_src)
                css = '/* ' + scss_path + ' */\n' + css
                return css
            except IOError:
                pass
        return ''

    def _load(self):
        path = os.path.join(self.block_dir, 'block.json')
        try:
            with open(path, 'r') as f:
                self._src = json.load(f)
        except IOError as e:
            print >> sys.stderr, "Error loading " + self.block_dir
            self._src = {}
        except Exception as e:
            print >> sys.stderr, "Error loading " + self.block_dir
            raise e
