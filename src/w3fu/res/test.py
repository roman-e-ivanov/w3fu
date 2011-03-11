from w3fu.res import bind, Resource
from w3fu.res.middleware.transform import json, xml
from w3fu.web import Response
from w3fu.web.forms import Form, IntArg


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

    t_from = IntArg('from', default=0)
    t_to = IntArg('to', default=0)


class Plan(Resource):

    def get(self, req):
        form = PlanForm(req.query)
        try:
            plan = PLAN_DATA[req.args['id']]
        except KeyError:
            return req.response(404)
        body = dict(filter(lambda (k, v): form.data['t_from'] <= k < form.data['t_to'], plan['body'].iteritems()))
        return Response(200, {'head': plan['head'], 'body': body.values()})


@bind('/api/plans/{id}', id='\d+')
class PlanJson(Plan):

    get = json()(Plan.get)


@bind('/plans/{id}', id='\d+')
class PlanXml(Plan):

    get = xml('test-html')(Plan.get)


@bind('/test')
class TestHtml(Resource):

    @xml('test-html')
    def get(self, req):
        return Response(200, {})
