from w3fu.routing import Route

from app.resources import Resource


class Index(Resource):

    route = Route('/')

    _block_path = 'pages/index'
