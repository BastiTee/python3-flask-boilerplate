# -*- coding: utf-8 -*-

"""Handle incoming API requests."""

import logging
from enum import Enum

from .utils import add_two_numbers


class ApiHandler():
    """API backend."""

    def __init__(self):  # noqa: D107
        self.logger = logging.getLogger(__name__)
        self.logger.info('Initializing API handler...')
        self.words = []

    def handle(self, operation, request_args=None, *args, **kwargs):
        """Dispatch incoming API requests."""
        if operation is ApiOperations.MESSAGE_GET:
            return 'This get endpoint does nothing. Sorry.'

        if operation is ApiOperations.MESSAGE_POST:
            num_1 = int(request_args.get('num1'))
            num_2 = int(request_args.get('num2'))
            if not num_1 or not num_2:
                return 'Invalid numbers'
            result = add_two_numbers(num_1, num_2)
            return f'{num_1} + {num_2} = {result}'


class ApiOperations(Enum):
    """Supported API operations."""

    MESSAGE_GET = 1
    MESSAGE_POST = 2
