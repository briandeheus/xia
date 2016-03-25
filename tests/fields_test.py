from xia import fields


def test_base_field():
    field = fields.BaseField()

    try:
        field.value = 'heh'
    except NotImplementedError, e:
        assert e


def test_integer_field():
    field = fields.IntegerField(max_val=10, min_val=0)
    field.value = 5

    assert field.value == 5

    try:
        field.value = 11
    except ValueError, e:
        assert e

    try:
        field.value = -1
    except ValueError, e:
        assert e

    try:
        field.value = 'not an integer'
    except ValueError, e:
        assert e


def test_string_field():
    field = fields.StringField(max_len=10)
    field.value = '123456789'

    assert field.value == '123456789'

    try:
        field.value = '12345678900'
    except ValueError, e:
        assert e


def test_pk_field():
    field = fields.PKField()
    field.value = 'Hue'
