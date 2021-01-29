class ApiException(Exception):
    def __init__(self, errors=[], *args, **kwargs):
        super(ApiException, self).__init__(*args, **kwargs)
        self.errors = errors


class RequestDataException(Exception):
    def __init__(self, errors=[], *args, **kwargs):
        super(RequestDataException, self).__init__(*args, **kwargs)
        self.errors = errors


class NotEnoughFundsException(ApiException):
    def __init__(self, errors=[], *args, **kwargs):
        super(NotEnoughFundsException, self).__init__(*args, **kwargs)
        self.errors = errors
