from decimal import Decimal

from flask.ext.testing import TestCase

from bank_api import create_app
from bank_api.extensions import db
from bank_api.tools.database import create_tables
from tests.factories import AccountFactory


class BaseTest(TestCase):

    def create_app(self):
        """
        Creates the test app
        """
        self.app = create_app(settings_override={
            'SQLALCHEMY_DATABASE_URI': 'sqlite://'
        })
        self.app.config['TESTING'] = True
        self.header = {'Content-Type': 'application/json'}
        return self.app

    def setUp(self):
        with self.app.app_context():
            create_tables(db)

    def create_account(self, balance='100.00', transactions=None, **kwargs):
        """
        Creates a test account with some basic data
        :param balance:
        :param transactions:
        :param kwargs:
        :return: Account object
        """
        if not transactions:
            transactions = []

        account = AccountFactory(
            balance=Decimal(balance),
            transactions=transactions,
            **kwargs
        )
        db.session.add(account)
        db.session.commit()
        return account
