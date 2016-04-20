# xia
A set of Tornado Classes for writing APIs with consistent response formats.

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

## Detailed example

```
class MyApi(xia.api.BaseApi):

    REQUIRED_GET_FIELDS = {
        'user_id': xia.fields.IntegerField(max_val=10000, min_val=1)
    }

    def get(self):

        self.write_response({
            'user': int(self.get_query_argument('user_id'))
        })

```

Request:
```
GET http://localhost/
```

Response:
```
{
  "error": {
    "blame": "user_id",
    "message": "Field is missing",
    "type": "FieldMissingException"
  }
}
```

Request:
```
GET http://localhost/?user_id=10001
```

Response:
```
{
  "error": {
    "blame": "user_id",
    "message": "Value can not be higher than 10000",
    "type": "ValueInvalidException"
  }
}
```

Request:
```
GET http://localhost/?user_id=abc
```

Response:
```
{
  "error": {
    "blame": "user_id",
    "message": "Value is not an integer",
    "type": "ValueInvalidException"
  }
}
```

Request:
```
GET http://localhost/?user_id=-1
```

Response:
```
{
  "error": {
    "blame": "user_id",
    "message": "Value can not be lower than 1",
    "type": "ValueInvalidException"
  }
}
```

Request:
```
GET localhost:8888/?user_id=5
```

Response:
```
{
  "data": {
    "user": 5
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

### Setup.py
`python setup.py test`

### With coverage

Be sure to have installed the following PIP packages.

* Tornado
* Nose
* Coverage

`nosetests --with-coverage --cover-package=xia`