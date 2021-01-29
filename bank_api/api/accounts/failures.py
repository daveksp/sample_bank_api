from ..common.failures import Failure


class Failures(object):

    insufficiente_funds = Failure({
        "error_category": "account_restriction",
        "error_type": "funds_error",
        "message": "Nao existe saldo suficiente para esta transacao.",
        "details": None
    })

    limit_exceeded = Failure({
        "error_category": "account_restriction",
        "error_type": "limit_exceeded_error",
        "message": "Esta transação ultrapassa o limite permitido.",
        "details": None
    })

    blocked_account = Failure({
        "error_category": "account_restriction",
        "error_type": "blocked_account_error",
        "message": "Esta operação não é permitida.",
        "details": "Operação não permitida, conta bloqueada. Consulte seu gerente."
    })
