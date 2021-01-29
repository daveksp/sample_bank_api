from flask import abort
from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import make_response
from flask import request
from flask_restful import Api
from flask_restful import Resource

from bank_api.api.accounts.schema import BalanceSchema
from bank_api.api.accounts.schema import AccountSchema
from bank_api.api.accounts.schema import StatementSchema
from bank_api.api.transactions.service import get_transactions
from bank_api.extensions import db
from bank_api.models import Account
from bank_api.models import Filters


blueprint = Blueprint('accounts', __name__, url_prefix='/accounts')
api = Api(blueprint)


@api.resource('/balance/<account_id>', endpoint='balance')
@api.resource('')
class AccountsResource(Resource):

    def post(self):
        """ Create an account """
        account_schema = AccountSchema()
        account, request_errors = account_schema.load(request.json or {})

        db.session.add(account)
        db.session.commit()

        response, response_errors = account_schema.dump(account)
        return make_response(jsonify(response), 201)

    def get(self, account_id):
        """retrieves balance"""
        account = Account.query.get(account_id)
        if not account:
            current_app.logger.exception(f"Account with id={account_id} not found")
            abort(404)

        balance_schema = BalanceSchema()
        response, response_errors = balance_schema.dump(account)
        return make_response(jsonify(response), 200)


@api.resource('/block/<account_id>', endpoint='block')
class ActionsResource(Resource):

    def delete(self, account_id):
        """block an account"""
        account = Account.query.get(account_id)
        if not account:
            current_app.logger.exception(f"Account with id={account_id} not found")
            abort(404)

        account.active_flag = False
        db.session.commit()

        account_schema = AccountSchema(only=("id", "person.name", "status"))
        response, response_errors = account_schema.dump(account)
        return make_response(jsonify(response), 200)


@api.resource('/statement/<account_id>', endpoint='statement')
class StatementsResource(Resource):

    def get(self, account_id):
        """retrieves statement"""
        filters = Filters(
            limit=int(request.args.get('limit', 0)),
            offset=int(request.args.get('offset', 0)),
            _from=str(request.args.get('from', '')),
            _to=str(request.args.get('to', ''))
        )
        current_app.logger.exception(f"loaded filters= {filters}")
        query = Account.query.filter(
            Account.id == account_id,
        )

        account = query.first()
        if not account:
            current_app.logger.info(f"Account with id={account_id} not found")
            abort(404)

        account.transactions = get_transactions(
            account_id, filters=filters
        ).all()
        statement_schema = StatementSchema()
        response, response_errors = statement_schema.dump(account)
        return make_response(jsonify(response), 200)
