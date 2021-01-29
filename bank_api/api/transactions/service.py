from datetime import datetime

from sqlalchemy import extract

from bank_api.api.accounts.validators import validate_account_state
from bank_api.api.accounts.validators import validate_daily_limit
from bank_api.api.common.validators import validate_monetary_value
from bank_api.api.transactions.validators import validate_funds
from bank_api.models import Transaction
from bank_api.models import TransactionTypeEnum


def get_transactions(account_id, transaction_type=None, filters=None):
    """get account transactions
    :param account_id:
    :param transaction_type:
    :param filters:
    :return: query object
    """
    query = Transaction.query.filter(Transaction.account_id == account_id)
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)

    if not filters:
        return query

    if filters._from and filters._to:
        query = query.filter(Transaction.transaction_date.between(
            filters._from, filters._to)
        )

    query = query.limit(filters.limit) if filters.limit else query
    query = query.offset(filters.offset) if filters.offset else query
    return query


def get_today_withdraws(account_id):
    """get current date withdraws total value.
    :param account_id:
    :return: Decimal value
    """
    today = datetime.today()
    query = get_transactions(
        account_id, transaction_type="withdraw"
    )
    # I had to leave like this, cause for sake of simplicity the tests are
    # being performed on sqlite, and it doesn't support normal date operations.
    # for this reason I also kept the code here instead of moving it to
    # `get_transactions`, so at least it'd look cleaner.
    query = query.filter(
        extract('year', Transaction.transaction_date) == today.year,
        extract('month', Transaction.transaction_date) == today.month,
        extract('day', Transaction.transaction_date) == today.day
    )
    return sum([transaction.value for transaction in query.all()])


def deposit(transaction):
    """deposits money into account
    :param transaction:
    :return:
    """
    transaction.account.balance += transaction.value


def withdraw(transaction):
    """deducts money from account's balance.
    :param transaction:
    :return:
    """
    total_transactions = get_today_withdraws(transaction.account_id)

    # calling multiple validators in order to maximize re-usability.
    # validate monetary_value once again just in case some is trying to change the
    # value through command line
    validate_monetary_value(transaction.value, 'value')
    validate_account_state(transaction.account)
    validate_funds(transaction)
    validate_daily_limit(transaction.account, total_transactions)

    transaction.account.balance -= transaction.value
