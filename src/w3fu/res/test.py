from w3fu.res import bind, Resource
from w3fu.res.snippets import json, html
from w3fu.res.middleware.transform import JSON, XML
from w3fu.web.forms import Form, IntArg


PLAN_DATA = {
             '1': {
                   'head': {
                            'step': '300'
                            },
                   'body': {
                            1298884200: 1,
                            1298884500: 0,
                            1298885100: 1,
                            }
                   },
             '2': {
                   'head': {
                            'step': '600'
                            },
                   'body': {
                            }
                   },
             }


class PlanForm(Form):

    t_from = IntArg('from', default=0)
    t_to = IntArg('to', default=0)


@bind('/api/plans/{id}', id='\d+')
class PlanJson(Resource):

    @JSON()
    def get(self, req):
        form = PlanForm(req.query)
        try:
            plan = PLAN_DATA[req.args['id']]
        except KeyError:
            return req.response(404)
        body = dict(filter(lambda (k, v): form.data['t_from'] <= k < form.data['t_to'], plan['body'].iteritems()))
        return req.response(200, {'head': plan['head'], 'body': body})


@bind('/test')
class TestHtml(Resource):

    @XML('test-html')
    def get(self, req):
        return req.response(200, {})
