import uuid


class BaseField(object):

    def __init__(self, *args, **kwargs):
        self._value = None

        if 'optional' in kwargs:
            self.__setattr__('optional', kwargs.get('optional'))

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.validate(value)
        self._value = value

    def validate(self, value):
        raise NotImplementedError

    pass


class PKField(BaseField):

    def __init__(self, *args, **kwargs):

        super(PKField, self).__init__(*args, **kwargs)

    def validate(self, value):

        if self._value is None:
            self._value = uuid.uuid4()


class IntegerField(BaseField):

    def __init__(self, min_val, max_val, *args, **kwargs):

        super(IntegerField, self).__init__(*args, **kwargs)

        self.min_val = min_val
        self.max_val = max_val
        self._value = None

    def validate(self, value):

        try:
            value = int(value)
        except ValueError:
            raise ValueError('Value [%s] is not an integer' % value)

        if value > self.max_val:
            raise ValueError('Value [%s] can not be higher than %s' % (self.max_val, value))

        if value < self.min_val:
            raise ValueError('Value [%s] can not be lower than %s' % (self.min_val, value))


class StringField(BaseField):

    def __init__(self, max_len, *args, **kwargs):

        super(StringField, self).__init__(*args, **kwargs)

        self.max_len = max_len

    def validate(self, value):

        value = str(value)

        if len(value) > self.max_len:
            raise ValueError('Value [%s] can not be longer than %s' % (value, self.max_len))


class ObjectField(BaseField):

    def __init__(self, fields, *args, **kwargs):

        super(ObjectField, self).__init__(*args, **kwargs)

        self.fields = fields

    def validate(self, value, parent=None):

        for field in self.fields:

            try:
                self.fields[field].validate(value[field])
            except KeyError:
                raise ValueError('Missing key [%s]' % field)
