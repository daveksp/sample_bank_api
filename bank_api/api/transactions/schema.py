from marshmallow import post_load
from marshmallow import validates
import simplejson

from bank_api.api.transactions.failures import Failures
from bank_api.api.messages import transaction_type_error
from bank_api.api.common.failures import Failures as CommonFailures
from bank_api.api.common.validators import validate_monetary_value

from bank_api.api.exceptions import ApiException
from bank_api.api.exceptions import RequestDataException
from bank_api.api.extensions import schemas

from bank_api.models import TransactionTypeEnum
from bank_api.models import Transaction


class TransactionSchema(schemas.Schema):

    id = schemas.Integer(required=True, dump_only=True)
    value = schemas.Decimal(required=True)
    transaction_date = schemas.Date(required=True, dump_only=True)
    description = schemas.String(required=True)
    account_id = schemas.Integer(required=True)
    transaction_type = schemas.String(required=True)

    class Meta:
        json_module = simplejson

    def handle_error(self, exc, data):
        response = CommonFailures.information_missing
        response['details'] = exc.messages
        raise RequestDataException(response)

    @validates('value')
    def validate_transaction_value(self, value):
        validate_monetary_value(value, 'value')

    @validates('transaction_type')
    def validate_transaction_type(self, transaction_type):
        if transaction_type not in TransactionTypeEnum.list():
            response = Failures.unsupported_operation
            response['details'] = transaction_type_error.format(
                transaction_type
            )
            raise ApiException(response)

    @post_load
    def make_order(self, data):
        return Transaction(**(data or {}))