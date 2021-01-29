from bank_api.models import Account
from bank_api.models import Person
from bank_api.models import Transaction


DB_MODELS = [Account, Person, Transaction]


def recreate_db(db, bind='__all__', app=None):
    """
    Drop existing tables and create new ones according to the current schema.
    """
    db.drop_all(bind=bind, app=app)
    db.create_all(bind=bind, app=app)


def create_tables(db, bind='__all__', app=None):
    """
    Create all missing tables according to the current schema.
    """
    db.create_all(bind=bind, app=app)
