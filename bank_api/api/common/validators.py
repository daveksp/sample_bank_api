from datetime import datetime

from bank_api.api.messages import date_field_error
from bank_api.api.messages import monetary_field_error
from bank_api.api.common.failures import Failures
from bank_api.api.exceptions import RequestDataException


def validate_date(date, field_name):
    """Check if date is bigger than current date.
    :param date:
    :param field_name: field name to be included in the error message
    :raises: RequestDataException
    :return:
    """
    if date > datetime.now().date():
        response = Failures.inconsistent_information
        response['details'] = date_field_error.format(field_name)

        raise RequestDataException(response)


def validate_monetary_value(value, field_name):
    """Check if monetary value is negative.
    :param value:
    :param field_name: field name to be included in the error message
    :raises: RequestDataException
    :return:
    """
    if value < 0:
        response = Failures.inconsistent_information
        response['details'] = monetary_field_error.format(field_name)

        raise RequestDataException(response)
