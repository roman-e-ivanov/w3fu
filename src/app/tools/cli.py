from wsgiref.util import setup_testing_defaults

from app import config, application


environ = {'HTTP_HOST': config.cli_http_host,
           'REQUEST_METHOD': config.cli_request_method,
           'PATH_INFO': config.cli_path_info,
           'HTTP_COOKIE': config.cli_http_cookie,
           'QUERY_STRING': config.cli_query_string}

setup_testing_defaults(environ)
application.debug(environ)
