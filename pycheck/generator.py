import sys
import string
import random

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

MIN_INT = -sys.maxint - 1
MAx_INT = sys.maxint

MAX_STR = 255
MAX_UNI = sys.maxunicode

# ------------------------------------------------------------------------------
# Generators
# ------------------------------------------------------------------------------

class Generator(object):
    def __init__(self, num_calls):
        self._calls_remaining = num_calls

    def __iter__(self):
        return self

    def next(self):
        if self._calls_remaining <= 0:
            raise StopIteration
        else:
            self._calls_remaining -= 1
            return self.nextValue()

class StringGenerator(Generator):
    def nextValue(self):
        length = random.randint(0, 40)
        return ''.join([chr(random.randint(0, MAX_STR)) for x in xrange(length)])

class IntGenerator(Generator):
    def nextValue(self):
        return random.randint(MIN_INT, MAx_INT)