from decimal import Decimal

from bank_api.api.accounts.failures import Failures as AccountFailures
from bank_api.api.exceptions import ApiException
from bank_api.models import TransactionTypeEnum
from bank_api.models import Transaction
from bank_api.api.transactions.validators import validate_funds
from tests.base import BaseTest


class ValidatorsTests(BaseTest):

    def test_validate_funds(self):
        """ validate_funds: check if no exception is raised when transaction
        value is not greater than the available balance.
        """
        # given
        account = self.create_account(
            balance="20.00",
            daily_withdraw_limit=Decimal("20.00")
        )
        transaction = Transaction(
            value=Decimal("10.00"), transaction_type=TransactionTypeEnum.withdraw,
            account=account
        )

        # when
        response = validate_funds(transaction)

        # then
        self.assertIsNone(response)

    def test_validate_funds_insufficient_funds(self):
        """ validate_funds:check if exception is raised when transaction
        value is greater than the available balance.
        """
        # given
        account = self.create_account(
            balance="10.00",
            daily_withdraw_limit=Decimal("20.00")
        )
        transaction = Transaction(
            value=Decimal("15.00"), transaction_type=TransactionTypeEnum.withdraw,
            account=account
        )

        # when
        with self.assertRaises(ApiException) as error_context:
            validate_funds(transaction)

        # then
        exception = error_context.exception
        self.assertEqual(exception.errors, AccountFailures.insufficiente_funds)
