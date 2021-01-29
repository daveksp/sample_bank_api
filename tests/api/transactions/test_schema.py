from unittest import TestCase

from bank_api.api.common.failures import Failures as CommonFailures
from bank_api.api.exceptions import ApiException
from bank_api.api.exceptions import RequestDataException
from bank_api.api.messages import operation_type_error
from bank_api.api.transactions.failures import Failures
from bank_api.api.transactions.schema import TransactionSchema
from tests.data_sample import get_transaction_data
from tests.utils import get_schema_required_fields


INVALID_TRANSACTION_TYPE = 'INVALID'


class SchemaTests(TestCase):

    def setUp(self) -> None:
        self.schema = TransactionSchema()

    def test_load(self):
        """ load: check if schama loads data without errors"""
        # given
        data = get_transaction_data()

        # when
        transaction, errors = self.schema.load(data)

        # then
        self.assertIsNotNone(transaction)
        self.assertFalse(errors)

    def test_load_missing_fields(self):
        """ load: check if schema raises errors if any required field is
        missing
        """
        # given
        data = get_transaction_data()
        required_fields = get_schema_required_fields(TransactionSchema)
        [data.pop(k) for k in required_fields]

        # when
        with self.assertRaises(RequestDataException) as error_context:
            _, _ = self.schema.load(data)

        # then
        self.assertEqual(
            set(error_context.exception.errors['details'].keys()) -
            set(required_fields),
            set([]))
        error_context.exception.errors['details'] = None
        self.assertEqual(
            error_context.exception.errors, CommonFailures.information_missing
        )

    def test_load_invalid_transaction_type(self):
        """ load: check if schema raises exception if invalid transaction
        type is provided.
        """
        # given
        expected_msg = operation_type_error.format(INVALID_TRANSACTION_TYPE)
        data = get_transaction_data()
        data['transaction_type'] = INVALID_TRANSACTION_TYPE

        # when
        with self.assertRaises(ApiException) as error_context:
            _, _ = self.schema.load(data)

        # then
        exception = error_context.exception
        self.assertEqual(exception.errors['details'], expected_msg)
        exception.errors['details'] = None
        self.assertEqual(exception.errors, Failures.unsupported_operation)
