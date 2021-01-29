from datetime import datetime
from decimal import Decimal

from mock import patch

from bank_api.api.accounts.failures import Failures as AccountFailures
from bank_api.api.exceptions import ApiException
from bank_api.api.messages import daily_withdraw_limit
from bank_api.api.transactions.service import deposit
from bank_api.api.transactions.service import get_today_withdraws
from bank_api.api.transactions.service import get_transactions
from bank_api.api.transactions.service import withdraw
from bank_api.models import Filters
from bank_api.models import Transaction
from bank_api.models import TransactionTypeEnum
from tests.base import BaseTest
from tests.factories import TransactionFactory


class ServiceTests(BaseTest):

    def test_deposit(self):
        """deposit: check if no exception is raised when deposit transaction
        is okay.
        """
        value = Decimal("20.00")
        account = self.create_account(balance=value)
        transaction = Transaction(
            value=Decimal(value), transaction_type=TransactionTypeEnum.withdraw,
            account=account
        )
        deposit(transaction)
        self.assertEqual(account.balance, Decimal("40.00"))

    def test_get_transactions_no_filters(self):
        """get_transactions: check if all account transactions are
        returned when no filter is provided.
        """
        # given
        number_transactions = 2
        account = self.create_account(
            balance=Decimal("20.00"),
            transactions=TransactionFactory.create_batch(number_transactions)
        )

        # when
        query = get_transactions(account.id)

        # then
        self.assertEqual(number_transactions, query.count())

    def test_get_transactions_filter_operation(self):
        """get_transactions: check if all account transactions are
        returned when filtering by transaction_type.
        """
        # given
        transactions = [
            TransactionFactory(transaction_type=TransactionTypeEnum.withdraw),
            TransactionFactory(transaction_type=TransactionTypeEnum.deposit)
        ]
        account = self.create_account(
            transactions=transactions
        )

        # when
        query = get_transactions(
            account.id, transaction_type=TransactionTypeEnum.withdraw
        )

        # then
        self.assertEqual(1, query.count())

    def test_get_transactions_filter_date(self):
        """get_transactions: check if corrent number of transactions are
        returned when filtering by date.
        """
        # given
        transactions = [
            TransactionFactory(
                transaction_type=TransactionTypeEnum.withdraw,
                transaction_date=datetime(2020, 12, 15)
            ),
            TransactionFactory(
                transaction_type=TransactionTypeEnum.deposit,
                transaction_date=datetime(2020, 12, 16)
            ),
            TransactionFactory(
                transaction_type=TransactionTypeEnum.deposit,
                transaction_date=datetime(2020, 12, 19)
            )
        ]

        account = self.create_account(transactions=transactions)

        # when
        filters = Filters(_from='2020-12-12', _to='2020-12-18')
        query = get_transactions(
            account.id, filters=filters
        )

        # then
        self.assertEqual(2, query.count())

    def test_get_today_withdraws(self):
        """get_today_withdraws: check if only current date withdraws are
        returned.
        """
        # given
        value = Decimal("5.00")
        transactions = [
            TransactionFactory(
                transaction_type=TransactionTypeEnum.withdraw,
                transaction_date=datetime.today(),
                value=value
            ),
            TransactionFactory(
                transaction_type=TransactionTypeEnum.withdraw,
                transaction_date=datetime.today(),
                value=value
            ),
            TransactionFactory(
                transaction_type=TransactionTypeEnum.withdraw,
                transaction_date=datetime(2020, 12, 19),
                value=value
            )
        ]
        account = self.create_account(transactions=transactions)

        # when
        current_total = get_today_withdraws(account.id)

        # then
        self.assertEqual(2 * value, current_total)

    @patch('bank_api.api.transactions.service.get_today_withdraws')
    def test_withdraw(self, mock_withdraws):
        """withdraw: check if withdraw operation is successfully executed."""
        # given
        mock_withdraws.return_value = Decimal("20.00")
        transaction = TransactionFactory(
            transaction_type=TransactionTypeEnum.withdraw,
            transaction_date=datetime.today(),
            value=Decimal("10.00"),
        )
        account = self.create_account(
            balance=Decimal("50.00"),
            transactions=[transaction],
            daily_withdraw_limit=Decimal("30.00")
        )

        # when
        withdraw(transaction)

        # then
        self.assertEqual(account.balance, Decimal("40.00"))

    @patch('bank_api.api.transactions.service.get_today_withdraws')
    def test_withdraw_insuficient_funds(self, mock_withdraws):
        """withdraw: check if exception is raised when there's no enough
        funds.
        """
        # given
        mock_withdraws.return_value = Decimal("0.00")
        account = self.create_account(
            balance=Decimal("20.00"),
            daily_withdraw_limit=Decimal("30.00")
        )
        transaction = TransactionFactory(
            transaction_type=TransactionTypeEnum.withdraw,
            transaction_date=datetime.today(),
            value=Decimal("30.00"),
            account=account
        )

        # when
        with self.assertRaises(ApiException) as error_context:
            withdraw(transaction)

        # then
        exception = error_context.exception
        self.assertEqual(exception.errors, AccountFailures.insufficiente_funds)

    @patch('bank_api.api.transactions.service.get_today_withdraws')
    def test_withdraw_blocked_acount(self, mock_withdraws):
        """withdraw: check if exception is raised when trying to take money
        from a blocked account.
        """
        # given
        mock_withdraws.return_value = Decimal("0.00")
        account = self.create_account(
            daily_withdraw_limit=Decimal("30.00"),
            active_flag=False
        )

        transaction = TransactionFactory(
            transaction_type=TransactionTypeEnum.withdraw,
            transaction_date=datetime.today(),
            value=Decimal("1.00"),
            account=account
        )

        # when
        with self.assertRaises(ApiException) as error_context:
            withdraw(transaction)

        # then
        exception = error_context.exception
        self.assertEqual(exception.errors, AccountFailures.blocked_account)

    @patch('bank_api.api.transactions.service.get_today_withdraws')
    def test_withdraw_limit_exceeded(self, mock_withdraws):
        """withdraw: check if exception is raised when current date
        transaction + transaction value exceeds daily limit.
        """
        # given
        mock_withdraws.return_value = Decimal("40.00")
        account = self.create_account(
            balance=Decimal("50.00"),
            daily_withdraw_limit=Decimal("30.00"),
        )

        # this is better tested in the endpoints. Since here we are mocking
        # daily_value. We can probably remove it!
        transaction = TransactionFactory(
            transaction_type=TransactionTypeEnum.withdraw,
            transaction_date=datetime.today(),
            value=Decimal("30.00"),
            account=account
        )

        # when
        with self.assertRaises(ApiException) as error_context:
            withdraw(transaction)

        # then
        exception = error_context.exception
        self.assertEqual(exception.errors['details'], daily_withdraw_limit)
        exception.errors['details'] = None
        self.assertEqual(exception.errors, AccountFailures.limit_exceeded)
