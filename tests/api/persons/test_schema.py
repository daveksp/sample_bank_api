from unittest import TestCase

from bank_api.api.messages import cpf_error
from bank_api.api.accounts.schema import PersonSchema
from bank_api.api.common.failures import Failures as CommonFailures
from bank_api.api.exceptions import RequestDataException
from tests.data_sample import get_person_data
from tests.utils import get_schema_required_fields


INVALID_CPF = '11223344'
VALID_UNMASKED_CPF = '11122233344'


class SchemaTests(TestCase):

    def setUp(self) -> None:
        self.schema = PersonSchema()

    def test_person_load_missing_fields(self):
        """ load: check if schema raises errors if any required field is
        missing
        """
        # given
        data = get_person_data()
        required_fields = get_schema_required_fields(PersonSchema)
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

    def test_person_load_unmasked_cpf(self):
        """ load: check if schama loads data without errors for a given
        unmasked CPF"""
        # given
        data = get_person_data()
        data["cpf"] = VALID_UNMASKED_CPF

        # when
        person, errors = self.schema.load(data)

        # then
        self.assertIsNotNone(person)
        self.assertFalse(errors)

    def test_person_load_invalid_cpf(self):
        """ load: check if schama raises errors for a invalid CPF"""
        # given
        data = get_person_data()
        data["cpf"] = INVALID_CPF
        expected_msg = cpf_error

        # when
        with self.assertRaises(RequestDataException) as error_context:
            _, _ = self.schema.load(data)

        # then
        exception = error_context.exception
        self.assertEqual(exception.errors['details'], expected_msg)
        exception.errors['details'] = None
        self.assertEqual(
            exception.errors, CommonFailures.inconsistent_information
        )
