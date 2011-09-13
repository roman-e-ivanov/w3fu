from w3fu.web.resources import Route, Resource
from w3fu.web.base import Response
from w3fu.web.forms import Form, IntArg

from app.resources.middleware.transform import json, xml


PLAN_DATA = {
             '1': {
                   'head': {
                            'step': 300
                            },
                   'body': {
                            1298884200: {'from': 1298884200, 'type': 1},
                            1298884500: {'from': 1298884500, 'type': 0},
                            1298885100: {'from': 1298885100, 'type': 1}
                            }
                   },
             '2': {
                   'head': {
                            'step': 600
                            },
                   'body': {
                            }
                   },
             }


class PlanForm(Form):

    t_from = IntArg('from')
    t_to = IntArg('to')


class Plan(Resource):

    def get(self, req):
        form = PlanForm(req.query)
        try:
            plan = PLAN_DATA[req.args['id']]
        except KeyError:
            return req.response(404)
        body = dict(filter(lambda (k, v): form.data['t_from'] <= k < form.data['t_to'], plan['body'].iteritems()))
        return Response(200, {
                              'id': req.args['id'],
                              'from': form.data['t_from'],
                              'to': form.data['t_to'],
                              'head': plan['head'],
                              'body': body.values()
                              })


class PlanJson(Plan):

    route = Route('/api/plans/{id}', id='\d+')
    get = json()(Plan.get)


class PlanXml(Plan):

    route = Route('/plans/{id}', id='\d+')
    get = xml('test-html.xsl')(Plan.get)


class TestHtml(Resource):

    route = Route('/test')

    @xml('test-html.xsl')
    def get(self, req):
        return Response(200, {})
