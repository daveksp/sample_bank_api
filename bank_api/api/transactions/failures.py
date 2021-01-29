from ..common.failures import Failure


class Failures(object):

    unsupported_operation = Failure({
        "error_category": "transaction_restriction",
        "error_type": "unsupported_operation",
        "message": "Operação não realizada.",
        "details": None
    })
