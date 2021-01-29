from datetime import datetime

import factory
from factory.fuzzy import FuzzyChoice
from factory.fuzzy import FuzzyDate
from factory.fuzzy import FuzzyDecimal
from factory.fuzzy import FuzzyText

from bank_api.models import Account
from bank_api.models import AccountTypeEnum
from bank_api.models import Person
from bank_api.models import Transaction
from bank_api.models import TransactionTypeEnum


class PersonFactory(factory.Factory):
    class Meta:
        model = Person

    name = FuzzyText(length=20)
    cpf = FuzzyText(length=11, chars='0123456789')
    birthdate = FuzzyDate(
        datetime(1980, 1, 1), datetime(2010, 1, 1)
    )
    email = factory.LazyAttribute(
        lambda a: '{}@example.com'.format(a.name.replace(' ', '.')).lower()
    )


class AccountFactory(factory.Factory):
    class Meta:
        model = Account

    person = factory.SubFactory(PersonFactory)
    balance = FuzzyDecimal(10.0, 100.0, 3)
    daily_withdraw_limit = FuzzyDecimal(5.0, 10.0, 3)
    active_flag = True
    account_type = FuzzyChoice([
        AccountTypeEnum.individual, AccountTypeEnum.company
    ])


class TransactionFactory(factory.Factory):
    class Meta:
        model = Transaction

    transaction_type = FuzzyChoice([
        TransactionTypeEnum.deposit, TransactionTypeEnum.withdraw
    ])
    description = FuzzyText(length=60)
