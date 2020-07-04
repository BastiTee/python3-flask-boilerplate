# -*- coding: utf-8 -*-

"""Handle incoming API requests."""

import json
import logging

from flask import abort, jsonify, make_response

from . import db


class ApiHandler():
    """API backend."""

    def __init__(self):  # noqa: D107
        self.logger = logging.getLogger(__name__)
        self.logger.info('Initializing API handler...')

    def get(self, request, *args, **kwargs):  # noqa: D102
        db_handle = db.get_db()
        rows = db_handle.execute('SELECT * from word;').fetchall()
        db_handle.close()
        return json.dumps([dict(ix) for ix in rows])

    def post(self, request, *args, **kwargs):  # noqa: D102
        data = request.get_json()
        word = data.get('word', None)
        if not word:
            return abort(400)
        db_handle = db.get_db()
        db_handle.execute(
            'INSERT INTO word (word) VALUES (?);',
            (word,),
        )
        db_handle.commit()
        db_handle.close()
        return jsonify([word])

    def delete(self, request, *args, **kwargs):  # noqa: D102
        db_handle = db.get_db()
        db_handle.execute('DELETE FROM word;')
        db_handle.commit()
        db_handle.close()
        return make_response(jsonify({}), 200)
