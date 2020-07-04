# -*- coding: utf-8 -*-
"""Module init-file.

The __init__.py files are required to make Python treat directories
containing the file as packages.
"""

import logging
import os

from flask import Flask

from . import db
from .api_handler import ApiHandler
from .api_routes import ApiRoutes

logging.basicConfig(
    # See https://docs.python.org/3/library/logging.html#logrecord-attributes
    format='%(asctime)-15s %(levelname)s %(message)s [%(name)s.%(funcName)s]',
    level=logging.INFO
)
# Disable werkzeug logging. we don't have it in production so don't rely on it
logging.getLogger('werkzeug').setLevel(logging.ERROR)


def create_app(test_config=None):
    """Flask application factory method."""
    logger = logging.getLogger(__name__)

    logger.info('Setting up Flask application...')
    app = Flask(__name__, instance_relative_config=True)

    logger.info('Setting up database...')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    logger.info('Setting up routes...')
    ApiRoutes(app, ApiHandler())

    logger.info('Server successfully started.')
    return app
