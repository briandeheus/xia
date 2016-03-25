import tornado.web
from exceptions import \
    FieldMissingException, \
    InvalidMethodException, \
    FormattingException, \
    NotFoundException, \
    ValueInvalidException

import json


class BaseApi(tornado.web.RequestHandler):

    REQUIRED_FIELDS = {}

    def __init__(self, *args, **kwargs):

        super(BaseApi, self).__init__(*args, **kwargs)

        self._error = None
        self._data = None

    def invalid_method(self):
        raise InvalidMethodException(self.request.method)

    def write_error(self, *args, **kwargs):

        e = kwargs["exc_info"][1].serialize()

        self.set_error(e['type'], e['message'], e['blame'])
        self.crap_out()

    def set_error(self, error_type, message, blame):
        self._error = {
            'type': error_type,
            'message': message,
            'blame': blame
        }

    def set_data(self, data):
        self._data = data

    def crap_out(self, code=400):
        self.set_status(code)
        self.finalize()
        self.finish()

    def validate(self):

        for field in self.REQUIRED_FIELDS:

            if self.get_argument(field, None) is None:
                raise FieldMissingException(field)

            try:
                self.request.arguments[field] = self.REQUIRED_FIELDS[field].validate(self.get_argument(field))
            except ValueError, e:
                raise ValueInvalidException(blame=field, message=e.message)

    def finalize(self):
        response = {}

        if self._error is not None:
            response['error'] = self._error
        elif self._data is not None:
            response['data'] = self._data

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(response))

    def prepare(self):

        if self.request.method == 'GET':

            self.validate()
            return

        if self.request.body is None or self.request.body == '':

            self.validate()
            return

        try:

            json_data = json.loads(self.request.body)
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

    def head(self, *args, **kwargs):
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

    def head(self, *args, **kwargs):
        self.not_found()

    def patch(self, *args, **kwargs):
        self.not_found()

    def put(self, *args, **kwargs):
        self.not_found()

    def delete(self, *args, **kwargs):
        self.not_found()
