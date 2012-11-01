from datetime import timedelta


blocks_dir = ''
static_dir = ''
js_root_block = 'js'
css_root_block = 'css'
static_formats = ['html']
media_extensions = frozenset(['.png', '.jpg', '.gif'])

cli_http_host = 'localhost'
cli_request_method = 'GET'
cli_path_info = '/'
cli_query_string = ''
cli_http_cookie = ''

db_uri = 'mongodb://localhost'
db_name = 'w3fu'

session_cookie = 'u'
session_ttl = timedelta(days=1)
