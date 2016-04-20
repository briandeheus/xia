from tornado.testing import AsyncHTTPTestCase
from xia import api, fields, exceptions

import json
import tornado.web


class TestApi(api.BaseApi):

    REQUIRED_GET_FIELDS = {
        'string': fields.StringField(max_len=128),
        'integer': fields.IntegerField(max_val=10, min_val=0)
    }

    REQUIRED_PUT_FIELDS = {
        'different_string': fields.StringField(max_len=128)
    }

    def get(self):
        self.write_response('haha')

    def put(self):
        self.write_response('haha')


class AuthApi(api.BaseApi):

    def auth(self):
        raise exceptions.ForbiddenException()

    def get(self):
        self.write_response('never seeing this')


class BreakApi(api.BaseApi):

    def get(self):
        raise SystemError('Oh no something went wrong woo be us')


class ObjectApi(api.BaseApi):

    REQUIRED_POST_FIELDS = {
        'object': fields.ObjectField(fields={
            'str': fields.StringField(max_len=128),
            'object2': fields.ObjectField(fields={
                'int': fields.IntegerField(max_val=10, min_val=0)
            })
        })
    }

    def post(self):
        self.write_response('haha')


class TestBase(AsyncHTTPTestCase):

    def setUp(self):
        super(TestBase, self).setUp()

    def get_app(self):
        self.app = tornado.web.Application([
            (r'/', TestApi),
            (r'/break', BreakApi),
            (r'/object', ObjectApi),
            (r'/auth', AuthApi),
            (r'/404', api.NotFoundApi),
            (r'/base', api.BaseApi),
        ])

        return self.app

    def call_url(self, url, method='GET', body=None):

        response = self.fetch(url, method=method, body=body, allow_nonstandard_methods=True)
        return response, json.loads(response.body)


class TestApiHandler(TestBase):

    def missing_params_test(self):

        response, obj = self.call_url('/')
        assert obj['error']['type'] == 'FieldMissingException'

        response, obj = self.call_url('/?string=huehue')
        assert obj['error']['type'] == 'FieldMissingException'

        response, obj = self.call_url('/?string=huehue&integer=-1')
        assert obj['error']['type'] == 'ValueInvalidException'

        response, obj = self.call_url('/?string=huehue&integer=5')
        assert obj['data'] == 'haha'

    def invalid_value_test(self):

        response, obj = self.call_url('/')
        assert obj['error']['type'] == 'FieldMissingException'

        response, obj = self.call_url('/?string=huehue')
        assert obj['error']['type'] == 'FieldMissingException'

        response, obj = self.call_url('/?string=huehue&integer=-1')
        assert obj['error']['type'] == 'ValueInvalidException'

        response, obj = self.call_url('/?string=huehue&integer=-1', 'POST', '{not; json}')
        assert obj['error']['type'] == 'FormattingException'

        response, obj = self.call_url('/?string=huehue&integer=5', 'POST', '{"this": "json"}')
        assert obj['error']['type'] == 'InvalidMethodException'

        response, obj = self.call_url('/?string=huehue&integer=5', 'PUT', '{"this": "json"}')
        assert obj['error']['type'] == 'FieldMissingException'

        response, obj = self.call_url('/', 'PUT', '{"different_string": "huehue"}')
        assert obj['data'] == 'haha'

        response, obj = self.call_url('/?string=huehue&integer=5')
        assert obj['data'] == 'haha'

    def not_found_test(self):

        response, obj = self.call_url('/404')
        assert obj['error']['type'] == 'NotFoundException'
        assert response.code == 404

        response, obj = self.call_url('/404', 'POST')
        assert obj['error']['type'] == 'NotFoundException'
        assert response.code == 404

        response, obj = self.call_url('/404', 'GET')
        assert obj['error']['type'] == 'NotFoundException'
        assert response.code == 404

        response, obj = self.call_url('/404', 'OPTIONS')
        assert obj['error']['type'] == 'NotFoundException'
        assert response.code == 404

        response, obj = self.call_url('/404', 'PATCH')
        assert obj['error']['type'] == 'NotFoundException'
        assert response.code == 404

        response, obj = self.call_url('/404', 'PUT')
        assert obj['error']['type'] == 'NotFoundException'
        assert response.code == 404

        response, obj = self.call_url('/404', 'DELETE')
        assert obj['error']['type'] == 'NotFoundException'
        assert response.code == 404

    def not_implemented_test(self):

        response, obj = self.call_url('/base', 'POST')
        assert obj['error']['type'] == 'InvalidMethodException'
        assert response.code == 400

        response, obj = self.call_url('/base', 'GET')
        assert obj['error']['type'] == 'InvalidMethodException'
        assert response.code == 400

        response, obj = self.call_url('/base', 'OPTIONS')
        assert obj['error']['type'] == 'InvalidMethodException'
        assert response.code == 400

        response, obj = self.call_url('/base', 'PATCH')
        assert obj['error']['type'] == 'InvalidMethodException'
        assert response.code == 400

        response, obj = self.call_url('/base', 'PUT')
        assert obj['error']['type'] == 'InvalidMethodException'
        assert response.code == 400

        response, obj = self.call_url('/base', 'DELETE')
        assert obj['error']['type'] == 'InvalidMethodException'
        assert response.code == 400

    def break_test(self):

        response, obj = self.call_url('/break', 'GET')
        assert obj['error']['type'] == 'SystemError'
        assert response.code == 500

    def forbidden_test(self):

        response, obj = self.call_url('/auth', 'GET')
        assert obj['error']['type'] == 'ForbiddenException'
        assert response.code == 403

    def object_api_test(self):

        valid_object = {
            'object': {
                'str': 'Hello World',
                'object2': {
                    'int': 10
                }
            }
        }

        response, obj = self.call_url('/object?test=true', 'POST', json.dumps(valid_object))
        assert obj['data'] == 'haha'

        invalid_object = {
            'object': {
                'str': 'Hello World',
                'object2': {
                    'int': 11
                }
            }
        }

        response, obj = self.call_url('/object', 'POST', json.dumps(invalid_object))
        assert obj['error']['type'] == 'ValueInvalidException'

        invalid_object = {
            'object': 'not and object'
        }

        response, obj = self.call_url('/object', 'POST', json.dumps(invalid_object))
        assert obj['error']['type'] == 'ValueInvalidException'

        invalid_object = {
            'object': [1, 2, 3]
        }

        response, obj = self.call_url('/object', 'POST', json.dumps(invalid_object))
        assert obj['error']['type'] == 'ValueInvalidException'
