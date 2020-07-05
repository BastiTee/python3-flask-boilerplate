# -*- coding: utf-8 -*-
"""Basic flask test suite."""

import json
import os
import tempfile

import my_module

import pytest

SAMPLE_WORD = {
    'word': 'testword'
}


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


def test_empty_db(__client):  # noqa: D103
    response = __client.get('/')
    assert response.status_code == 200
    assert json.loads(response.data) == []


def test_insert_and_get_one(__client):  # noqa: D103
    response = __client.post(
        '/',
        data=json.dumps(SAMPLE_WORD),
        content_type='application/json'
    )
    assert response.status_code == 200
    response = __client.get('/')
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['word'] == 'testword'


def test_insert_delete_and_get_none(__client):  # noqa: D103
    response = __client.post(
        '/',
        data=json.dumps(SAMPLE_WORD),
        content_type='application/json'
    )
    assert response.status_code == 200
    response = __client.delete()
    assert response.status_code == 200
    response = __client.get('/')
    data = json.loads(response.data)
    assert len(data) == 0
