# -*- coding: utf-8 -*-

"""Handle incoming API requests."""

import logging
from enum import Enum
from random import choice

from .utils import get_kwarg_value_or_empty


class ApiHandler():
    """API backend."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info('Initializing API handler...')
        self.words = []

    def handle(self, operation, *args, **kwargs):
        """Dispatch incoming API requests."""
        if operation is ApiOperations.MESSAGE_GET:
            if not self.words or len(self.words) == 0:
                return 'List of words is empty'
            word = choice(list(self.words))
            self.words.remove(word)
            return f'Your word is \'{word}\'. Words left: {len(self.words)}'

        if operation is ApiOperations.MESSAGE_POST:
            new_words = get_kwarg_value_or_empty(kwargs, 'message').split(',')
            new_words = [word.strip() for word in new_words]
            self.words = set(list(self.words) + new_words)
            return (f'Added new words: {new_words}. '
                    + f'Total words now {len(self.words)}')


class ApiOperations(Enum):

    MESSAGE_GET = 1
    MESSAGE_POST = 2
