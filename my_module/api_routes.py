# -*- coding: utf-8 -*-
# pylint: disable=W0612

"""REST API routes."""

import logging
from time import time

from flask import abort, request


class ApiRoutes():
    """Available API routes for this web application."""

    def __init__(self, app, api_handler):  # noqa: D107

        self.logger = logging.getLogger(__name__)

        @app.route('/', methods=['GET'])
        def get():
            return api_handler.get(request)

        @app.route('/', methods=['POST'])
        def post():
            if request.is_json:
                return api_handler.post(request)
            else:
                return abort(400)

        @app.route('/', methods=['DELETE'])
        def delete():
            return api_handler.delete(request)

        @app.before_request
        def before_request():
            request.now = time()

        @app.after_request
        def after_request(response):
            runtime = round((time() - request.now) * 1000, 2)
            content = [
                request.method,
                request.path,
                request.query_string.decode('utf-8'),
                request.remote_addr,
                str(response.status_code),
                '|',
                str(response.content_length),
                response.charset,
                response.content_type,
                '|',
                str(runtime) + ' ms'
            ]
            self.logger.info(' '.join(content))
            return response
