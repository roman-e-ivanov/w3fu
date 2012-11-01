from app import config
from app.view import blocks


for fmt in ['html']:
    blocks[config.css_root_block].make_css(fmt, config.static_dir)
    blocks[config.js_root_block].make_js(fmt, config.static_dir)
