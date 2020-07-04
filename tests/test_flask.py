# -*- coding: utf-8 -*-
"""Basic flask test suite."""

import json
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
    response = __client.get('/')
    assert response.status_code == 200
    assert json.loads(response.data) == []
