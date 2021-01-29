from marshmallow import post_load
from marshmallow import validates
import simplejson

from bank_api.api.common.failures import Failures as CommonFailures
from bank_api.api.common.validators import validate_monetary_value
from bank_api.api.transactions.schema import TransactionSchema
from bank_api.api.persons.schema import PersonSchema
from bank_api.api.exceptions import RequestDataException
from bank_api.api.extensions import schemas
from bank_api.models import Account


class BalanceSchema(schemas.Schema):
    id = schemas.Integer(required=True, dump_only=True)
    balance = schemas.Decimal(required=False)
    person = schemas.Nested(PersonSchema, only=['name'])

    class Meta:
        json_module = simplejson


class StatementSchema(schemas.Schema):
    id = schemas.Integer(required=True, dump_only=True)
    balance = schemas.Decimal(required=False)
    person = schemas.Nested(PersonSchema, only=['name'])
    transactions = schemas.Nested(TransactionSchema, required=False, many=True)

    class Meta:
        json_module = simplejson


class AccountSchema(schemas.Schema):
    id = schemas.Integer(required=True, dump_only=True)
    person = schemas.Nested(
        PersonSchema, exclude=['id'], required=True
    )
    balance = schemas.Decimal(required=False)
    daily_withdraw_limit = schemas.Decimal(required=True)
    status = schemas.String(dump_only=True)
    created_at = schemas.Date(required=True, dump_only=True)
    account_type = schemas.String(required=True)

    class Meta:
        json_module = simplejson

    def handle_error(self, exc, data):
        response = CommonFailures.information_missing
        response['details'] = exc.messages
        raise RequestDataException(response)

    @validates('daily_withdraw_limit')
    def validate_daily_withdraw_limit(self, withdraw_limit):
        validate_monetary_value(withdraw_limit, 'daily_withdraw_limit')

    @validates('balance')
    def validate_initial_balance(self, balance):
        validate_monetary_value(balance, 'balance')

    @post_load
    def make_order(self, data):
        return Account(**(data or {}))
