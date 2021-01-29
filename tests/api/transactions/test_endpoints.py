from decimal import Decimal
import json

from bank_api.api.accounts.failures import Failures as AccountFailures
from bank_api.api.messages import daily_withdraw_limit
from tests.base import BaseTest
from tests.data_sample import get_transaction_data


class TransactionsResourceTests(BaseTest):

    def test_post_deposito(self):
        # given
        account = self.create_account()
        balance = account.balance
        transaction_data = get_transaction_data()
        transaction_value = Decimal(transaction_data['value'])
        transaction_data['account_id'] = account.id

        # when
        response = self.app.test_client().post(
            '/transactions', data=json.dumps(transaction_data),
            headers=self.header)
        response_data = json.loads(response.data)

        # then
        self.assertTrue(response_data['transaction_date'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(account.balance, balance + transaction_value)

    def test_post_saque_limit_exceeded(self):
        # given
        account = self.create_account(daily_withdraw_limit=Decimal('50.00'))

        transaction_data = get_transaction_data()
        transaction_data['transaction_type'] = 'withdraw'
        transaction_data['value'] = '60.00'
        transaction_data['account_id'] = account.id

        # when
        response = self.app.test_client().post(
            '/transactions', data=json.dumps(transaction_data),
            headers=self.header)
        response_data = json.loads(response.data)
        expected_response = AccountFailures.limit_exceeded
        expected_response['details'] = daily_withdraw_limit

        # then
        self.assert400(response)
        self.assertEqual(response_data['error'], expected_response)

    def test_post_saque_blocked_account(self):
        # given
        account = self.create_account(active_flag=False)
        transaction_data = get_transaction_data()
        transaction_data['transaction_type'] = 'withdraw'
        transaction_data['value'] = '10.00'
        transaction_data['account_id'] = account.id

        # when
        response = self.app.test_client().post(
            '/transactions', data=json.dumps(transaction_data),
            headers=self.header)
        response_data = json.loads(response.data)

        # then
        self.assert400(response)
        self.assertEqual(
            response_data['error'], AccountFailures.blocked_account
        )

    def test_post_saque_insufficient_funds(self):
        # given
        account = self.create_account(
            balance=Decimal('200.00'), daily_withdraw_limit=Decimal('1000.00')
        )

        transaction_data = get_transaction_data()
        transaction_data['transaction_type'] = 'withdraw'
        transaction_data['value'] = '1000.00'
        transaction_data['account_id'] = account.id

        # when
        response = self.app.test_client().post(
            '/transactions', data=json.dumps(transaction_data),
            headers=self.header)
        response_data = json.loads(response.data)

        # then
        self.assert400(response)
        self.assertEqual(
            response_data['error'], AccountFailures.insufficiente_funds
        )

    def test_post_deposito_account_not_found(self):
        # given
        transaction_data = get_transaction_data()

        # when
        response = self.app.test_client().post(
            f'/transactions/99',
            data=json.dumps(transaction_data),
            headers=self.header
        )
        json.loads(response.data)

        # then
        self.assert404(response)
