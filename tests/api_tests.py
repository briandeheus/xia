from tornado.testing import AsyncHTTPTestCase
from xia import api, fields

import json
import tornado.web


class TestApi(api.BaseApi):

    REQUIRED_FIELDS = {
        'string': fields.StringField(max_len=128),
        'integer': fields.IntegerField(max_val=10, min_val=0)
    }

    def get(self):
        self.set_data('haha')
        self.finalize()

    def put(self):
        self.set_data('haha')
        self.finalize()


class TestBase(AsyncHTTPTestCase):

    def setUp(self):
        super(TestBase, self).setUp()

    def get_app(self):
        self.app = tornado.web.Application([
            (r'/', TestApi),
            (r'/404', api.NotFoundApi)
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
        assert obj['data'] == 'haha'

        response, obj = self.call_url('/?string=huehue&integer=5')
        assert obj['data'] == 'haha'

    def not_found_test(self):

        response, obj = self.call_url('/404')
        assert obj['error']['type'] == 'NotFoundException'

        response, obj = self.call_url('/404', 'POST')
        assert obj['error']['type'] == 'NotFoundException'

        response, obj = self.call_url('/404', 'GET')
        assert obj['error']['type'] == 'NotFoundException'

        response, obj = self.call_url('/404', 'OPTIONS')
        assert obj['error']['type'] == 'NotFoundException'

        response, obj = self.call_url('/404', 'PATCH')
        assert obj['error']['type'] == 'NotFoundException'

        response, obj = self.call_url('/404', 'PUT')
        assert obj['error']['type'] == 'NotFoundException'

        response, obj = self.call_url('/404', 'DELETE')
        assert obj['error']['type'] == 'NotFoundException'