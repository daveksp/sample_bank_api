from datetime import datetime
import json

from bank_api.api.constants import ACTIVE_VALUE
from bank_api.api.constants import BLOCKED_VALUE
from bank_api.models import Account
from tests.base import BaseTest
from tests.factories import TransactionFactory
from tests.data_sample import get_account_data


class AccountsResourceTests(BaseTest):

    def test_post(self):
        """post: check post endpoint works just fine"""
        # given
        data = get_account_data()

        # when
        response = self.app.test_client().post(
            '/accounts', data=json.dumps(data),
            headers=self.header)
        response_data = json.loads(response.data)

        # then
        self.assertTrue(response_data['created_at'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['status'], ACTIVE_VALUE)

    def test_get_balance(self):
        """get: check balance is returned for a valid account"""
        # given
        account = self.create_account()

        # when
        response = self.app.test_client().get(
            f'/accounts/balance/{account.id}',
        )
        response_data = json.loads(response.data)

        # then
        self.assert200(response)
        self.assertEqual(response_data['balance'], account.balance)
        self.assertEqual(response_data['id'], account.id)

    def test_get_balance_account_not_found(self):
        """get: check if 404 is received when account doesn't exist"""
        # given / when
        response = self.app.test_client().get(
            f'/accounts/balance/99',
        )
        json.loads(response.data)

        # then
        self.assert404(response)


class ActionsResourceResourceTests(BaseTest):

    def test_delete_block(self):
        """delete: check account gets successfully blocked"""
        # given
        account = self.create_account()

        # when
        response = self.app.test_client().delete(
            f'/accounts/block/{account.id}',
        )
        response_data = json.loads(response.data)

        # then
        reloaded_account = Account.query.get(account.id)
        self.assert200(response)
        self.assertEqual(response_data['status'], BLOCKED_VALUE)
        self.assertEqual(response_data['id'], account.id)
        self.assertFalse(reloaded_account.active_flag)

    def test_delete_block_account_not_found(self):
        """delete: check if 404 is received when account doesn't exist"""
        # given / when
        response = self.app.test_client().delete(
            f'/accounts/block/99',
        )
        json.loads(response.data)

        # then
        self.assert404(response)


class StatementsResourceTests(BaseTest):

    def test_get_statement(self):
        """get: check if statement is received for a valid account"""
        # given
        number_transactions = 5
        account = self.create_account(
            transactions=TransactionFactory.create_batch(number_transactions)
        )

        # when
        response = self.app.test_client().get(
            f'/accounts/statement/{account.id}',
        )
        response_data = json.loads(response.data)
        # then
        self.assert200(response)
        self.assertEqual(len(response_data['transactions']), len(account.transactions))
        self.assertEqual(response_data['id'], account.id)

    def test_get_statement_filter_by_period(self):
        """get: check if statement with transactions per period is received
        for a valid account
        """
        # given
        transactions = [
            TransactionFactory(transaction_date=datetime(2020, 12, 15)),
            TransactionFactory(transaction_date=datetime(2020, 12, 16)),
            TransactionFactory(transaction_date=datetime(2020, 12, 19))
        ]
        account = self.create_account(transactions=transactions)

        # when
        response = self.app.test_client().get(
            f'/accounts/statement/{account.id}?from=2020-12-14&to=2020-12-17',
        )
        response_data = json.loads(response.data)

        # then
        self.assert200(response)
        self.assertEqual(len(response_data['transactions']), 2)
        self.assertEqual(response_data['id'], account.id)

    def test_get_statement_paginated(self):
        """get: check if paginated statement is received for a valid account"""
        # given
        transactions = [
            TransactionFactory(transaction_date=datetime(2020, 12, 15)),
            TransactionFactory(transaction_date=datetime(2020, 12, 16)),
            TransactionFactory(transaction_date=datetime(2020, 12, 19))
        ]
        account = self.create_account(transactions=transactions)

        # when
        response = self.app.test_client().get(
            f'/accounts/statement/{account.id}?limit=1&offset=2',
        )
        response_data = json.loads(response.data)
        # then
        self.assert200(response)
        self.assertEqual(len(response_data['transactions']), 1)
        self.assertEqual(response_data['id'], account.id)

    def test_get_statement_not_found(self):
        """get: check if 404 is received when account doesn't exist"""
        # given / when
        response = self.app.test_client().get(
            f'/accounts/statement/99',
        )
        json.loads(response.data)

        # then
        self.assertEqual(response.status_code, 404)
