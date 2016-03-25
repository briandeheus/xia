import uuid


class BaseField(object):

    def __init__(self):
        self._value = None

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

    def __init__(self):

        super(PKField, self).__init__()

    def validate(self, value):

        if self._value is None:
            self._value = uuid.uuid4()


class IntegerField(BaseField):

    def __init__(self, min_val, max_val):

        super(IntegerField, self).__init__()

        self.min_val = min_val
        self.max_val = max_val
        self._value = None

    def validate(self, value):

        try:
            value = int(value)
        except ValueError:
            raise ValueError('Value is not an integer')

        if value > self.max_val:
            raise ValueError('Value can not be higher than %s' % self.max_val)

        if value < self.min_val:
            raise ValueError('Value can not be lower than %s' % self.min_val)


class StringField(BaseField):

    def __init__(self, max_len):

        super(StringField, self).__init__()

        self.max_len = max_len


    def validate(self, value):

        value = str(value)

        if len(value) > self.max_len:
            raise ValueError('Value can not be longer than %s' % self.max_len)
