from datetime import datetime
import enum

from .extensions import db
from sqlalchemy.orm import backref

from bank_api.api.constants import ACTIVE_VALUE
from bank_api.api.constants import BLOCKED_VALUE


class TransactionTypeEnum(enum.Enum):
    deposit = "deposito"
    withdraw = "saque"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))


class AccountTypeEnum(enum.Enum):
    individual = "pessoaFisica"
    company = "pessoaJuridica"


class Account(db.Model):
    __tablename__ = 'contas'

    id = db.Column(db.Integer, name='idConta', primary_key=True)
    person_id = db.Column(
        db.Integer,
        db.ForeignKey('pessoas.idPessoa'),
        name="idPessoa",
        nullable=False
    )
    person = db.relationship('Person', foreign_keys=person_id)
    balance = db.Column(db.DECIMAL(10, 2), name='saldo', default=0)
    daily_withdraw_limit = db.Column(
        db.DECIMAL(10, 2), name='limiteSaqueDiario', default=0
    )
    active_flag = db.Column(db.Boolean, name='flagAtivo', default=True)
    created_at = db.Column(
        db.DateTime,
        name='dataCriacao',
        default=datetime.now,
        nullable=False
    )

    account_type = db.Column(
        db.Enum(AccountTypeEnum),
        nullable=False,
        name='tipoConta',
        default=AccountTypeEnum.individual.value
    )

    transactions = db.relationship(
        "Transaction", backref=backref("account"), lazy="noload"
    )

    @property
    def status(self):
        return ACTIVE_VALUE if self.active_flag else BLOCKED_VALUE


class Person(db.Model):
    __tablename__ = 'pessoas'

    id = db.Column(db.Integer, name='idPessoa', primary_key=True)
    name = db.Column(db.String(60), name='nome', nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    birthdate = db.Column(
        db.DateTime,
        name='dataNascimento',
        default=datetime.now,
        nullable=False,
    )
    email = db.Column(db.String(80), unique=True)


class Transaction(db.Model):

    __tablename__ = 'transacoes'

    id = db.Column(db.Integer, name='idTransacao', primary_key=True)
    account_id = db.Column(
        db.Integer, db.ForeignKey('contas.idConta'), name='idConta'
    )
    value = db.Column(db.DECIMAL(10, 2), name='valor', default=0)
    transaction_date = db.Column(
        db.DateTime,
        name='dataTransacao',
        default=datetime.now,
        nullable=False,
        onupdate=datetime.now
    )
    transaction_type = db.Column(
        db.Enum(TransactionTypeEnum),
        name='tipoTransacao',
        nullable=False,
        default=TransactionTypeEnum.deposit.value
    )
    description = db.Column(db.String(80), name='descricao')


class Filters:

    _from = None
    _to = None
    limit = 50      # it's good to have a default limit.
    offset = 0

    def __init__(self, _from=None, _to=None, limit=None, offset=None):
        self._from = _from
        self._to = _to
        self.limit = limit
        self.offset = offset
