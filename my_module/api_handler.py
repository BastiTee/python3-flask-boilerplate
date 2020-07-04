# -*- coding: utf-8 -*-

"""Handle incoming API requests."""

import logging

from flask import jsonify

from . import db


class ApiHandler():
    """API backend."""

    def __init__(self):  # noqa: D107
        self.logger = logging.getLogger(__name__)
        self.logger.info('Initializing API handler...')

    def get(self, request, *args, **kwargs):  # noqa: D102
        cursor = db.get_db().cursor()
        cursor.execute('SELECT * from word')
        words = cursor.fetchall()
        cursor.close()
        return jsonify(words)

    def post(self, request, *args, **kwargs):  # noqa: D102
        print(request.data)
        return {}

    def delete(self, request, *args, **kwargs):  # noqa: D102
        return {}
