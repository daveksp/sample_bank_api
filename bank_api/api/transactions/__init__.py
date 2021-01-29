from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import make_response
from flask import request
from flask_restful import Api
from flask_restful import Resource

from bank_api.api.transactions.schema import TransactionSchema
from bank_api.api.transactions.service import deposit, withdraw
from bank_api.extensions import db
from bank_api.models import Account
from bank_api.models import TransactionTypeEnum


blueprint = Blueprint('transactions', __name__, url_prefix='/transactions')
api = Api(blueprint)


@api.resource('')
class TransactionsResource(Resource):

    OPERATIONS = {
        TransactionTypeEnum.withdraw.name: withdraw,
        TransactionTypeEnum.deposit.name: deposit,
    }

    def post(self):
        """ Create a transaction """
        transacao_schema = TransactionSchema()
        transacao, request_errors = transacao_schema.load(request.json or {})
        transacao.account = Account.query.get(transacao.account_id)

        response = self.OPERATIONS[transacao.transaction_type](transacao)
        db.session.add(transacao)
        db.session.commit()

        response, response_errors = transacao_schema.dump(transacao)
        return make_response(jsonify(response), 201)
