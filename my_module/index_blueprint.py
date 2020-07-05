# -*- coding: utf-8 -*-
"""REST API routes."""

import json
import logging
from time import time

from flask import Blueprint, abort, render_template, request

from .api_handler import ApiHandler

blue_print = Blueprint('index', __name__, url_prefix='/')
logger = logging.getLogger(__name__)
api_handler = ApiHandler()


def __is_accept(request, accept_type):
    accept_header = request.headers.get('Accept', '').lower()
    return accept_type in accept_header


@blue_print.route('/', methods=['GET'])
def __get():
    if __is_accept(request, 'text/html'):
        return render_template(
            'index.html',
            words=api_handler.get(request)
        )
    elif __is_accept(request, 'application/json'):
        return json.dumps(api_handler.get(request))
    else:
        abort(415)


@blue_print.route('/', methods=['POST'])
def __post():
    if request.is_json and __is_accept(request, 'application/json'):
        return api_handler.post(request)
    else:
        return abort(400)


@blue_print.route('/', methods=['DELETE'])
def __delete():
    return api_handler.delete(request)


@blue_print.before_request
def __before_request():
    request.now = time()


@blue_print.after_request
def __after_request(response):
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
    logger.info(' '.join(content))
    return response
