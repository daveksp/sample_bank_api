import re

from marshmallow import post_load
from marshmallow import validates
import simplejson

from bank_api.api.common.failures import Failures
from bank_api.api.common.validators import validate_date
from bank_api.api.constants import CPF_PATTERN
from bank_api.api.exceptions import RequestDataException
from bank_api.api.extensions import schemas
from bank_api.api.messages import cpf_error
from bank_api.models import Person


class PersonSchema(schemas.Schema):
    id = schemas.String(required=True, dump_only=True)
    name = schemas.String(required=True)
    cpf = schemas.String(required=True)
    birthdate = schemas.Date(required=True)
    email = schemas.Email(required=True)

    class Meta:
        json_module = simplejson

    def handle_error(self, exc, data):
        response = Failures.information_missing
        response['details'] = exc.messages
        raise RequestDataException(response)

    @validates('birthdate')
    def validate_birthdate(self, birthdate):
        validate_date(birthdate, 'birthdate')

    @validates('cpf')
    def validate_cpf(self, cpf):
        is_unmasked_cpf = cpf.isdigit() and len(cpf) == 11

        if not re.search(CPF_PATTERN, cpf) and not is_unmasked_cpf:
            response = Failures.inconsistent_information
            response['details'] = cpf_error
            raise RequestDataException(response)

    @post_load
    def make_pessoa(self, data):
        return Person(**(data or {}))
