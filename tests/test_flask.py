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


def __get_json(__client):
    response = __client.get('/', headers={
        'Accept': 'application/json'
    })
    assert response.status_code == 200
    return json.loads(response.data)


def __post_sample_word(__client):
    response = __client.post(
        '/',
        data=json.dumps({
            'word': 'testword'
        }),
        content_type='application/json',
        headers={
            'Accept': 'application/json'
        }
    )
    assert response.status_code == 200


def test_empty_db(__client):  # noqa: D103
    assert __get_json(__client) == []


def test_insert_and_get_one(__client):  # noqa: D103
    __post_sample_word(__client)
    # Get words
    data = __get_json(__client)
    assert len(data) == 1
    assert data[0]['word'] == 'testword'


def test_insert_delete_and_get_none(__client):  # noqa: D103
    __post_sample_word(__client)
    # Delete all words
    response = __client.delete()
    assert response.status_code == 200
    # Get words
    assert len(__get_json(__client)) == 0
