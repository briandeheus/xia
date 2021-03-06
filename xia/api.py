# -*- coding: utf-8 -*-
from __future__ import absolute_import


import json
import uuid

import tornado.web

from .exceptions import \
    FieldMissingException, \
    InvalidMethodException, \
    FormattingException, \
    NotFoundException, \
    ValueInvalidException, \
    APIException


class BaseApi(tornado.web.RequestHandler):

    REQUIRED_GET_FIELDS = {}
    REQUIRED_POST_FIELDS = {}
    REQUIRED_PUT_FIELDS = {}
    REQUIRED_PATCH_FIELDS = {}
    REQUIRED_DELETE_FIELDS = {}
    REQUIRED_OPTIONS_FIELDS = {}

    __FIELD_MAP = {
        'GET': REQUIRED_GET_FIELDS,
        'POST': REQUIRED_POST_FIELDS,
        'PUT': REQUIRED_PUT_FIELDS,
        'PATCH': REQUIRED_PATCH_FIELDS,
        'DELETE': REQUIRED_DELETE_FIELDS,
        'OPTIONS': REQUIRED_OPTIONS_FIELDS,
    }

    ENCODE = 'utf-8'

    def __init__(self, *args, **kwargs):

        super(BaseApi, self).__init__(*args, **kwargs)

        self._error = None
        self._data = None

        # Request ID that can be used for logging, auditing and debug purposes
        self.request_id = str(uuid.uuid4())

    def auth(self):
        pass

    def invalid_method(self):
        raise InvalidMethodException(self.request.method)

    def write_error(self, *args, **kwargs):

        e = kwargs["exc_info"][1]

        if isinstance(e, APIException):
            serialized = e.serialize()
            self.set_error(serialized['type'], serialized['message'], serialized['blame'])
            code = e.CODE

        else:
            self.set_error(e.__class__.__name__, str(e), 'server')
            code = 500

        self.crap_out(code=code)

    def set_error(self, error_type, message, blame):
        self._error = {
            'type': error_type,
            'message': message,
            'blame': blame,
            'request': self.request_id
        }

    def write_response(self, data):
        self._data = data
        self.finalize()

    def crap_out(self, code=400):
        self.set_status(code)
        self.finalize()
        self.finish()

    def validate(self):

        fields = getattr(self, 'REQUIRED_{}_FIELDS'.format(self.request.method))

        for field in fields:

            if field not in self.request.arguments:
                raise FieldMissingException(field)

            try:
                fields[field].validate(self.request.arguments[field])

            except ValueError as e:
                raise ValueInvalidException(blame=field, message=str(e))

    def finalize(self):
        response = {}

        if self._error is not None:
            response['error'] = self._error
        elif self._data is not None:
            response['data'] = self._data

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(response))

    def prepare(self):

        # Before anything else, authenticate.
        # We don't want to waste CPU cycles on unauthenticated requests.
        self.auth()

        self.request.arguments = {}

        for argument in self.request.query_arguments:
            self.request.arguments[argument] = self.request.query_arguments[argument][0]

        if self.request.method == 'GET':

            self.validate()
            return

        body = self.request.body.decode(self.__class__.ENCODE)
        if body is None or body == '':

            self.validate()
            return

        if body in self.request.arguments:
            del self.request.arguments[body]

        try:

            json_data = json.loads(body)
            self.request.arguments.update(json_data)

        except ValueError:

            raise FormattingException('request')

        self.validate()

    def post(self, *args, **kwargs):
        self.invalid_method()

    def get(self):
        self.invalid_method()

    def options(self, *args, **kwargs):
        self.invalid_method()

    def patch(self, *args, **kwargs):
        self.invalid_method()

    def put(self, *args, **kwargs):
        self.invalid_method()

    def delete(self, *args, **kwargs):
        self.invalid_method()


class NotFoundApi(BaseApi):

    def not_found(self):
        raise NotFoundException('request')

    def post(self, *args, **kwargs):
        self.not_found()

    def get(self, *args, **kwargs):
        self.not_found()

    def options(self, *args, **kwargs):
        self.not_found()

    def patch(self, *args, **kwargs):
        self.not_found()

    def put(self, *args, **kwargs):
        self.not_found()

    def delete(self, *args, **kwargs):
        self.not_found()
