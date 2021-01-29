from decimal import Decimal
from unittest import TestCase

from bank_api.api.accounts.failures import Failures
from bank_api.api.accounts.validators import validate_account_state
from bank_api.api.accounts.validators import validate_daily_limit
from bank_api.api.exceptions import ApiException
from bank_api.api.messages import daily_withdraw_limit
from bank_api.models import Account
from tests.base import BaseTest


class ValidatorsTests(BaseTest):

    def test_validate_account_state(self):
        """ validate_account_state: check if no exception is raised when
        account is active.
        """
        # given
        account = Account(active_flag=True)

        # when
        response = validate_account_state(account)

        # then
        self.assertIsNone(response)

    def test_validate_account_state_blocked(self):
        """validate_date: check if an exception is raised when account is
        blocked
        """
        # given
        account = Account(active_flag=False)

        # when
        with self.assertRaises(ApiException) as error_context:
            validate_account_state(account)

        # then
        exception = error_context.exception
        self.assertEqual(exception.errors, Failures.blocked_account)

    def test_validate_daily_limit(self):
        """ validate_daily_limit: check if no exception is raised when
        total value taken from account in the present date doesn't exceed
        the limit.
        """
        # given
        value = Decimal("10.00")
        account = self.create_account(daily_withdraw_limit=Decimal("20.00"))

        # when
        response = validate_daily_limit(account, value)

        # then
        self.assertIsNone(response)

    def test_validate_daily_limit_exceeded(self):
        """ validate_daily_limit: check if exception is raised when
        total value taken from account in the present date exceeds
        the limit.
        """
        # given
        value = Decimal("25.00")
        account = self.create_account(daily_withdraw_limit=Decimal("20.00"))

        # when
        with self.assertRaises(ApiException) as error_context:
            validate_daily_limit(account, value)

        # then
        exception = error_context.exception

        self.assertEqual(exception.errors['details'], daily_withdraw_limit)
        exception.errors['details'] = None
        self.assertEqual(exception.errors, Failures.limit_exceeded)
