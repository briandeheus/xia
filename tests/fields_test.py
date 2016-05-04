from xia import fields


def test_base_field():
    field = fields.BaseField()

    try:
        field.validate('heh')
    except NotImplementedError as e:
        assert e


def test_list_field():
    field = fields.ListField(max_len=5, min_len=1)
    has_error = False

    field.validate([1])

    try:
        field.validate([])
    except ValueError:
        has_error = True

    assert has_error
    has_error = False

    try:
        field.validate([1, 2, 3, 4, 5, 6])
    except ValueError:
        has_error = True

    assert has_error


def test_integer_field():
    field = fields.IntegerField(max_val=10, min_val=0)

    try:
        field.validate(11)
    except ValueError as e:
        assert e

    try:
        field.validate(-1)
    except ValueError as e:
        assert e

    try:
        field.validate('not an integer')
    except ValueError as e:
        assert e


def test_string_field():
    field = fields.StringField(max_len=10)
    field.validate('123456789')

    try:
        field.validate('12345678900')
    except ValueError as e:
        assert e


def test_object_field():

    field = fields.ObjectField(fields={
        'int': fields.IntegerField(max_val=10, min_val=0),
        'string': fields.StringField(max_len=10)
    })

    try:
        field.validate({
            'string': 'Hello'
        })

    except ValueError as e:
        assert e

    field.validate({
        'int': 5,
        'string': 'Hello'
    })
