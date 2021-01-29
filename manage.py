import click
from flask.cli import FlaskGroup

from bank_api.manage import create_tables_command, rebuilddb_command


def create_bank_app(info):
    from bank_api import create_app
    return create_app()


@click.group(cls=FlaskGroup, create_app=create_bank_app)
def cli():
    """This is a management script for the bank api."""


@cli.command(name='rebuilddb')
def rebuilddb():
    """create tables"""
    create_tables_command()


@cli.command(name='create_tables')
def create_tables():
    """rebuild db"""
    rebuilddb_command()


if __name__ == '__main__':
    cli()
