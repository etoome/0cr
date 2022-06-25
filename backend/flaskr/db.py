import sqlite3
import random, string

import click
from flask import current_app, g
from flask.cli import with_appcontext
from datetime import date


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        # print(f.read().decode('utf-8'))
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def generate_string(length):
    """
    Generates a string of given length
    """
    res = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    return res

def generate_int(max):
    """
    Returns an int between 0 and `max`
    """
    res = int(random.random() * (max + 1))
    return res

def generate_secret():
    """
    Generates a random 10 char string to assign as user secret
    """
    res = generate_string(10)
    return res

def user_exist(username):
    """
    Returns True if the user who's uswername is in the dabatase
    """
    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username=?", (username,)
    ).fetchone()

    if user is None:
        return False
    else:
        return True

def get_user_from_key(key):
    db = get_db()
    return db.execute(
        "SELECT * FROM user WHERE key=?", (key,)
    ).fetchone()

def get_game(**kwargs):
    """
    Finds a line in the game table by using the key of the token.
    If none of the arguments are given will return an error
    """

    if len(kwargs) != 1:
        raise ValueError("Only 1 argument 'key' or 'token' should be given")

    db = get_db()
    key, val = kwargs.popitem()

    # TODO: Understand why "SELECT ... ?=?", (key, val) doesn't work
    if key == 'key':
        res = db.execute(
            "SELECT * FROM game WHERE key=?", (val,)
        ).fetchone()
    elif key == 'token':
        res = db.execute(
            "SELECT * FROM game WHERE token=?", (val,)
        ).fetchone()
    else:
        raise ValueError("Only 'key' or 'token' are valid arguments")

    return res

def get_date():
    """
    Generates date string
    YYYY-MM-DD
    """
    today = date.today()
    return f"{today.year}-{today.month}-{today.day}"
