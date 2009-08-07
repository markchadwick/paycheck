import sys
import string
import random
from itertools import izip, islice

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

MIN_INT = -sys.maxint - 1
MAX_INT = sys.maxint

MAX_UNI = sys.maxunicode

LIST_LEN = 30

# ------------------------------------------------------------------------------
# Exceptions
# ------------------------------------------------------------------------------

class PayCheckException(Exception):
    pass

class UnknownTypeException(PayCheckException):
    def __init__(self, t_def):
        self.t_def = t_def
    
    def __str__(self):
        return "PayCheck doesn't know about type: " + str(self.t_def)

class IncompleteTypeException(PayCheckException):
    def __init__(self, t_def):
        self.t_def = t_def
    
    def __str__(self):
        return "The type specification '" + str(self.t_def) + " is incomplete."

# ------------------------------------------------------------------------------
# Base Generator
# ------------------------------------------------------------------------------

class PayCheckGenerator(object):
    def __iter__(self):
        return self
    
    @classmethod
    def get(cls, t_def):
        try:
            if isinstance(t_def, PayCheckGenerator):
                return t_def
            elif isinstance(t_def, type):
                return scalar_generators[t_def]()
            else:
                return container_generators[type(t_def)](t_def)
        except KeyError:
            raise UnknownTypeException(t_def)

# ------------------------------------------------------------------------------
# Basic Type Generators
# ------------------------------------------------------------------------------

class StringGenerator(PayCheckGenerator):
    def next(self):
        length = random.randint(0, LIST_LEN)
        return ''.join([chr(random.randint(ord('!'), ord('~'))) for x in xrange(length)])

class UnicodeGenerator(PayCheckGenerator):
    def next(self):
        length = random.randint(0, LIST_LEN)
        return ''.join([unicode(random.randint(0, MAX_UNI)) for x in xrange(length)])

class IntGenerator(PayCheckGenerator):
    def __init__(self, min=MIN_INT, max=MAX_INT):
        PayCheckGenerator.__init__(self)
        self._min = min
        self._max = max

    def next(self):
        return random.randint(self._min, self._max)

def irange(min,max):
    return IntGenerator(min,max)

class BooleanGenerator(PayCheckGenerator):
    def next(self):
        return random.randint(0, 1) == 1

class FloatGenerator(PayCheckGenerator):
    def next(self):
        return (random.random() - 0.5) * 9999999.0

class NonNegativeFloatGenerator(PayCheckGenerator):
    def next(self):
        return random.random() * 9999999.0
non_negative_float = NonNegativeFloatGenerator()

class PositiveFloatGenerator(NonNegativeFloatGenerator):
    def next(self):
        value = 0
        while value <= 0:
            value = random.random() * 9999999.0
        return value
positive_float = PositiveFloatGenerator()

# ------------------------------------------------------------------------------
# Collection Generators
# ------------------------------------------------------------------------------

class CollectionGenerator(PayCheckGenerator):
    def __init__(self, t_def):
        PayCheckGenerator.__init__(self)
        self.inner = PayCheckGenerator.get(t_def)
    
    def next(self):
        return self.to_container(islice(self.inner,random.randint(0,LIST_LEN)))

class ListGenerator(CollectionGenerator):
    def __init__(self, example):
        try:
            CollectionGenerator.__init__(self,iter(example).next())
        except StopIteration:
            raise IncompleteTypeException(example)

    def to_container(self,generator):
        return list(generator)

class SetGenerator(ListGenerator):
    def to_container(self,generator):
        return set(generator)

class DictGenerator(CollectionGenerator):
    def __init__(self, example):
        try:
            CollectionGenerator.__init__(self,example.iteritems().next())
        except StopIteration:
            raise IncompleteTypeException(example)

    def to_container(self,generator):
        return dict(generator)

class TupleGenerator(PayCheckGenerator):
    def __init__(self, example):
        PayCheckGenerator.__init__(self)
        self.generators = map(PayCheckGenerator.get,example)

    def __iter__(self):
        return izip(*self.generators)        
        
# ------------------------------------------------------------------------------
# Dictionary of Generators
# ------------------------------------------------------------------------------

scalar_generators = {
    str:     StringGenerator,
    int:     IntGenerator,
    unicode: UnicodeGenerator,
    bool:    BooleanGenerator,
    float:   FloatGenerator,
  }

container_generators = {
    list:    ListGenerator,
    dict:    DictGenerator,
    set:     SetGenerator,
    tuple:   TupleGenerator,
  }
