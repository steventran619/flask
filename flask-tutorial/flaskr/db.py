import sqlite3

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # This makes the connection return rows that behave like dicts.
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """
    Check if a connection was created by checking if g.db was set. 
    If exists, close the connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    # open_resource() opens a file relative to the flaskr package, 
    # which is useful since you won’t necessarily know where that location is 
    # when deploying the application later.
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    # tells Flask to call that function when cleaning up after returning 
    # the response.
    app.teardown_appcontext(close_db)
    # adds a new command that can be called with the flask command.
    app.cli.add_command(init_db_command)