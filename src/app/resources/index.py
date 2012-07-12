from w3fu.routing import Route

from app.view import templates
from app.resources import Resource


class Index(Resource):

    route = Route('/')

    _block = templates.block('pages/index')
