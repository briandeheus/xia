import uuid


class BaseField(object):
    pass


class PKField(BaseField):

    def __init__(self, value=None):
        self.value = value

    def validate(self):

        if self.value is None:
            self.value = uuid.uuid4()

        return self.value


class IntegerField(BaseField):

    def __init__(self, min_val, max_val, value=None):
        self.min_val = min_val
        self.max_val = max_val
        self.value = value

    def validate(self, value):

        try:
            value = int(value)
        except ValueError:
            raise ValueError('Value is not an integer')

        if value > self.max_val:
            raise ValueError('Value can not be higher than %s' % self.max_val)

        if value < self.min_val:
            raise ValueError('Value can not be lower than %s' % self.min_val)

        self.value = value
        return value


class StringField(BaseField):

    def __init__(self, max_len, value=None):
        self.max_len = max_len
        self.value = value

    def validate(self, value):

        value = str(value)

        if len(value) > self.max_len:
            raise ValueError('Value can not be longer than %s' % self.max_len)

        self.value = value
        return self.value

    def __unicode__(self):
        return self.value