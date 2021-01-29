from bank_api.extensions import db
from bank_api.tools.database import create_tables
from bank_api.tools.database import recreate_db


def rebuilddb_command():
    recreate_db(db)


def create_tables_command():
    create_tables(db)
