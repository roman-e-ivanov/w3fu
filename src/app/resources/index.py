from w3fu.routing import Route

from app.resources.base import BaseResource


class Index(BaseResource):

    route = Route('/')

    _block_path = 'pages/index'
