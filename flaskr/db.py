import psycopg2

import click
from flask import current_app, g, session
from flask.cli import with_appcontext

from . import DBWrapper


def init_db(app):
    print("INIT DB")
    db = get_db(app)


def get_db():
    print("GET DB")
    dbw = DBWrapper(
        host='40.85.80.197',
        dbname='aero',
        user='aero',
        password='domodedovo',
        port='5432'
    )
    return dbw


def close_db(e=None):
    print("CLOSE DB")
    return


def init_app(app):
    print("INIT APP")
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
