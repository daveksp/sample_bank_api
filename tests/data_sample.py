def get_person_data():
    return {
        "name": "John Doe",
        "cpf": "111.222.333-44",
        "birthdate": "2000-01-01",
        "email": "john.doe@email.com",
    }


def get_account_data():
    return {
        "person": get_person_data(),
        "balance": "100.00",
        "daily_withdraw_limit": "30.00",
        "active_flag": True,
        "account_type": "individual"
    }


def get_transaction_data():
    return {
        "id": 1,
        "value": "20.00",
        "transaction_type": "deposit",
        "description": "Mock transaction",
        "account_id": 1
    }
