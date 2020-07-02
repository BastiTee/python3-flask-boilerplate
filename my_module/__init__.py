# -*- coding: utf-8 -*-
"""Module init-file.

The __init__.py files are required to make Python treat directories
containing the file as packages.
"""

import logging

from flask import Flask

from .api_handler import ApiHandler, ApiOperations
from .api_routes import ApiRoutes

logging.basicConfig(
    # See https://docs.python.org/3/library/logging.html#logrecord-attributes
    format='%(asctime)-15s %(levelname)s %(message)s [%(name)s.%(funcName)s]',
    level=logging.INFO
)
# Disable werkzeug logging. we don't have it in production so don't rely on it
logging.getLogger('werkzeug').setLevel(logging.ERROR)


def create_app():
    """Flask application factory method."""
    logger = logging.getLogger(__name__)

    logger.info('Setting up Flask application...')
    app = Flask(__name__)
    ApiRoutes(app, ApiHandler(), ApiOperations)

    logger.info('Server successfully started.')
    return app
