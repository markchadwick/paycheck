import sys
import string
import random

from pycheck import NUM_CALLS

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

MIN_INT = -sys.maxint - 1
MAX_INT = sys.maxint

MAX_STR = 255
MAX_UNI = sys.maxunicode

LIST_LEN = 40

# ------------------------------------------------------------------------------
# Exceptions
# ------------------------------------------------------------------------------

class PyCheckException(Exception):
    pass

class UnknownTypeException(PyCheckException):
    def __init__(self, t_def):
        self.t_def = t_def
    
    def __str__(self):
        return "PyCheck doesn't know about type: " + str(self.t_def)

class UnknownTypeException(PyCheckException):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return str(self.message)

# ------------------------------------------------------------------------------
# Base Generator
# ------------------------------------------------------------------------------

class PyCheckGenerator(object):
    def __init__(self, num_calls=NUM_CALLS):
        self._calls_remaining = num_calls

    def __iter__(self):
        return self

    def next(self):
        if self._calls_remaining <= 0:
            raise StopIteration
        else:
            self._calls_remaining -= 1
            return self.nextValue()
    
    @classmethod
    def get(cls, t_def):
        if isinstance(t_def, type):
            return cls._generator_for_type(t_def)()
            
        elif isinstance(t_def, tuple) and len(t_def) == 2:
            outer, inner = t_def
            return cls._generator_for_type(outer)(cls.get(inner))
        
        else:
            raise UnknownTypeException(t_def)
        
    @classmethod
    def _generator_for_type(cls, t_def):
        assert isinstance(t_def, type)
        
        try:
            return {
                str:     StringGenerator,
                int:     IntGenerator,
                unicode: UnicodeGenerator,
                bool:    BooleanGenerator,
                list:    ListGenerator,
                dict:    DictGenerator
            }[t_def]
        except KeyError:
            raise UnknownTypeException(t_def)

# ------------------------------------------------------------------------------
# Basic Type Generators
# ------------------------------------------------------------------------------

class StringGenerator(PyCheckGenerator):
    def nextValue(self):
        length = random.randint(0, LIST_LEN)
        return ''.join([chr(random.randint(0, MAX_STR)) for x in xrange(length)])

class UnicodeGenerator(PyCheckGenerator):
    def nextValue(self):
        length = random.randint(0, LIST_LEN)
        return ''.join([unicode(random.randint(0, MAX_UNI)) for x in xrange(length)])

class IntGenerator(PyCheckGenerator):
    def nextValue(self):
        return random.randint(MIN_INT, MAX_INT)

class BooleanGenerator(PyCheckGenerator):
    def nextValue(self):
        return random.randint(0, 1) == 1
    
# ------------------------------------------------------------------------------
# Collection Generators
# ------------------------------------------------------------------------------

class ListGenerator(PyCheckGenerator):
    def __init__(self, inner=None, num_calls=NUM_CALLS):
        PyCheckGenerator.__init__(self, num_calls=num_calls)
        if inner is None:
            raise UnknownTypeException("PyCheck needs a type for lists, such " +
                                       "as (list, int) or (list, bool)")
        self.inner = inner
    
    def nextValue(self):
        length = random.randint(0, LIST_LEN)
        return [self.inner.nextValue() for x in xrange(length)]

def DictGenerator(PyCheckGenerator):
    def __init__(self, k_inner, v_inner, num_calls=NUM_CALLS):
        PyCheckGenerator.__init__(self, num_calls=num_calls)
        self.k_inner = k_inner
        self.v_inner = v_inner