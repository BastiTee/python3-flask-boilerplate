# -*- coding: utf-8 -*-
"""Database handler."""

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """Initialize database access."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Close database."""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Initialize database schema."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_app(app):
    """Initialize flask app context."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')