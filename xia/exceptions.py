class APIException(Exception):

    MESSAGE = 'An unknown error has occured'
    CODE = 400

    def __init__(self, blame=None, message=None):
        self.blame = blame
        self.message = message
        pass

    def serialize(self):
        return {
            'type': self.__class__.__name__,
            'message': self.message if self.message is not None else self.MESSAGE,
            'blame': self.blame
        }


class ForbiddenException(APIException):
    MESSAGE = "You do not have access to this API"
    CODE = 403


class NotFoundException(APIException):
    MESSAGE = 'This API does not exist'
    CODE = 404


class FormattingException(APIException):
    MESSAGE = 'We could not parse your request'


class InvalidMethodException(APIException):
    MESSAGE = 'This API can not be called with this method'


class FieldMissingException(APIException):
    MESSAGE = 'Field is missing'


class ValueInvalidException(APIException):
    MESSAGE = 'Field value is invalid'