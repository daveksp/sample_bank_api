from flask import current_app

from bank_api.api.accounts.failures import Failures
from bank_api.api.exceptions import NotEnoughFundsException


def validate_funds(transaction):
    if transaction.value > transaction.account.balance:
        current_app.logger.error(
            f"Account-{transaction.account.id} doesn't have enough funds:"
            f"balance={transaction.account.balance}, transaction_value={transaction.value}"
        )
        response = Failures.insufficiente_funds
        raise NotEnoughFundsException(response)
