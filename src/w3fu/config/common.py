from datetime import timedelta


xslt_ext_prefix = 'http://w3fu/'

domain = 'localhost'

cli_http_host = domain
cli_request_method = 'GET'
cli_path_info = '/register'
cli_query_string = ''
cli_http_cookie = ''

db_host = 'localhost'
db_port = 27017
db_name = 'w3fu'

session_cookie = 'u'
session_ttl = timedelta(days=1)
