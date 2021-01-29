from flask import current_app

from bank_api.api.accounts.failures import Failures
from bank_api.api.exceptions import ApiException
from bank_api.api.messages import daily_withdraw_limit


def validate_account_state(account):
    """Check if account is blocked.
    :param account:
    :return:
    """
    if not account.active_flag:
        current_app.logger.error(
            f"Account-{account.id} has activate_flag={account.active_flag}"
        )
        response = Failures.blocked_account
        raise ApiException(response)


def validate_daily_limit(account, current_daily_value):
    """check if withdraw daily limit was exceeded.
    :param account:
    :param current_daily_value:
    :return:
    """
    if current_daily_value > account.daily_withdraw_limit:
        current_app.logger.error(
            f"Account- {account.id} has/will exceed(ed) the daily limit"
            f" daily_total={current_daily_value}, limit={account.daily_withdraw_limit}"
        )
        response = Failures.limit_exceeded
        response['details'] = daily_withdraw_limit
        raise ApiException(response)
