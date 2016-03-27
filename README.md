# xia
Python Framework for writing APIs with consistent error reporting.

Xia replies always follow the same format for handling succesful requests:

```
{
  "data": "My Response"
}
```

But also when something doesn't go quite right:

```
{
  "error": {
    "blame": "user_id",
    "message": "Field value is invalid",
    "type": "ValueInvalidException"
  }
}
```

Or when something can't be found

```
{
  "error": {
    "blame": "/",
    "message": "This API does not exist",
    "type": "NotFoundException"
  }
}
```

Or create your own exceptions by extending existing exceptions!
```
{
  "error": {
    "blame": "everyone else but me",
    "message": "This is a custom exception!",
    "type": "CustomException"
  }
}
```

## Included Exceptions
```
class NotFoundException(APIException):
    MESSAGE = 'This API does not exist'
```

```
class FormattingException(APIException):
    MESSAGE = 'We could not parse your request'
```

```
class InvalidMethodException(APIException):
    MESSAGE = 'This API can not be called with this method'
```

```
class FieldMissingException(APIException):
    MESSAGE = 'Field is missing'
```

```
class ValueInvalidException(APIException):
    MESSAGE = 'Field value is invalid'
```

## Testing
nosetests --with-coverage --cover-package=xia