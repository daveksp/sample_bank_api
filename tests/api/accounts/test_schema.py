from unittest import TestCase

from bank_api.api.accounts.schema import AccountSchema
from bank_api.api.common.failures import Failures as CommonFailures
from bank_api.api.exceptions import RequestDataException
from tests.data_sample import get_account_data
from tests.utils import get_schema_required_fields


class SchemaTests(TestCase):

    def setUp(self) -> None:
        self.schema = AccountSchema()

    def test_account_load(self):
        """ load: check if schama loads data without errors"""
        # given
        data = get_account_data()

        # when
        account, errors = self.schema.load(data)

        # then
        self.assertIsNotNone(account)
        self.assertFalse(errors)

    def test_account_load_missing_fields(self):
        """ load: check if schema raises errors if any required field is
        missing
        """
        # given
        data = get_account_data()
        required_fields = get_schema_required_fields(
            AccountSchema
        )
        [data.pop(k) for k in required_fields]

        # when
        with self.assertRaises(RequestDataException) as error_context:
            _, _ = self.schema.load(data)

        # then
        self.assertEqual(
            set(error_context.exception.errors['details'].keys()) -
            set(required_fields),
            set([])
        )
        error_context.exception.errors['details'] = None
        self.assertEqual(
            error_context.exception.errors, CommonFailures.information_missing
        )
