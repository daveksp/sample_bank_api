from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from freezegun import freeze_time

from bank_api.api import messages
from bank_api.api.common.failures import Failures as CommonFailures
from bank_api.api.common.validators import validate_date
from bank_api.api.common.validators import validate_monetary_value
from bank_api.api.exceptions import RequestDataException


class ValidatorsTests(TestCase):

    @freeze_time('2021-01-01 12:01')
    def test_validate_date(self):
        """ validate_date: check if no exception is raised when date provided
        is older than current date.
        """
        # given
        field_name = 'my_date_field'
        future_date = datetime(2020, 1, 31).date()

        # when
        response = validate_date(future_date, field_name)

        # then
        self.assertIsNone(response)

    @freeze_time('2021-01-01 12:01')
    def test_validate_date_invalid_future_date(self):
        """validate_date: check if exception is raised when future date is
        provided
        """
        # given
        field_name = 'my_date_field'
        future_date = datetime(2021, 1, 5).date()
        expected_msg = messages.date_field_error.format(field_name)

        # when
        with self.assertRaises(RequestDataException) as error_context:
            validate_date(future_date, field_name)

        # then
        exception = error_context.exception

        self.assertEqual(exception.errors['details'], expected_msg)
        exception.errors['details'] = None
        self.assertEqual(
            exception.errors, CommonFailures.inconsistent_information
        )

    def test_validate_monetary_value(self):
        """ validate_monetary_value: check if no exception is raised when
        positive value is provided.
        """
        # given
        field_name = 'my_monetary_field'
        valid_value = Decimal("20.00")

        # when
        response = validate_monetary_value(valid_value, field_name)

        # then
        self.assertIsNone(response)

    def test_validate_monetary_value_negative_value(self):
        """ validate_monetary_value: check if exception is raised when
        negative value is provided.
        """
        # given
        field_name = 'my_monetary_field'
        valid_value = Decimal("-20.00")
        expected_msg = messages.monetary_field_error.format(field_name)

        # when
        with self.assertRaises(RequestDataException) as error_context:
            validate_monetary_value(valid_value, field_name)

        # then
        exception = error_context.exception

        self.assertEqual(exception.errors['details'], expected_msg)
        exception.errors['details'] = None
        self.assertEqual(
            exception.errors, CommonFailures.inconsistent_information
        )
