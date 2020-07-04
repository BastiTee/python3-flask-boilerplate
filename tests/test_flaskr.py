# -*- coding: utf-8 -*-
"""Basic flask test suite."""

import os
import tempfile

import my_module

import pytest


@pytest.fixture
def __client():
    app = my_module.create_app()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            my_module.db.init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_empty_db(__client):
    """Start with a blank database."""
    rv = __client.get('/')
    assert b'This get endpoint does nothing. Sorry.' in rv.data
