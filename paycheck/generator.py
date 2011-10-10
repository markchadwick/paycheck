import sys
import string
import random
from itertools import izip, islice
from math import log, exp, pi
import cmath

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

    def next(self):
        return self.__next__()
    
    @classmethod
    def get(cls, t_def):
        try:
            if isinstance(t_def, PayCheckGenerator):
                return t_def
            elif isinstance(t_def, type):
                if issubclass(t_def, PayCheckGenerator):
                    return t_def()
                else:
                    return scalar_generators[t_def]()
            else:
                return container_generators[type(t_def)](t_def)
        except KeyError:
            raise UnknownTypeException(t_def)

# ------------------------------------------------------------------------------
# Basic Type Generators
# ------------------------------------------------------------------------------

class StringGenerator(PayCheckGenerator):
    def __next__(self):
        length = random.randint(0, LIST_LEN)
        return ''.join([chr(random.randint(ord('!'), ord('~'))) for x in xrange(length)])

if sys.version_info[0] < 3:
    class UnicodeGenerator(PayCheckGenerator):
        def __next__(self):
            length = random.randint(0, LIST_LEN)
            return ''.join([unicode(random.randint(0, MAX_UNI)) for x in xrange(length)])

class IntGenerator(PayCheckGenerator):
    def __init__(self, min=MIN_INT, max=MAX_INT, step=1):
        PayCheckGenerator.__init__(self)
        self._min = min
        self._boundary = (max-min)//step
        self._step = step

    def __next__(self):
        return int(random.randint(0,self._boundary)*self._step+self._min)

def irange(min,max,step=1):
    return IntGenerator(min,max,step)

class BooleanGenerator(PayCheckGenerator):
    def __next__(self):
        return random.randint(0, 1) == 1

class UniformFloatGenerator(PayCheckGenerator):
    def __init__(self,min=-1e7,max=1e7):
        self._min = min
        self._length = max-min
        
    def __next__(self):
        return random.random()*self._length+self._min

frange = UniformFloatGenerator

unit_interval_float = frange(0,1)

class NonNegativeFloatGenerator(PayCheckGenerator):
    def __init__(self,minimum_magnitude=1e-7,maximum_magnitude=1e+7):
        minimum_magnitude = log(minimum_magnitude)
        maximum_magnitude = log(maximum_magnitude)
        self._scale_range = maximum_magnitude-minimum_magnitude
        self._minimum_magnitude = minimum_magnitude
    def __next__(self):
        return exp(random.random() * self._scale_range + self._minimum_magnitude)
non_negative_float = NonNegativeFloatGenerator

class PositiveFloatGenerator(NonNegativeFloatGenerator):
    def __next__(self):
        value = 0
        while value == 0:
            value = NonNegativeFloatGenerator.__next__(self)
        return value
positive_float = PositiveFloatGenerator

class FloatGenerator(NonNegativeFloatGenerator):
    def __next__(self):
        return NonNegativeFloatGenerator.__next__(self)*random.choice([+1,-1])

class ComplexGenerator(NonNegativeFloatGenerator):
    def __next__(self):
        return NonNegativeFloatGenerator.__next__(self) * cmath.exp(random.random()*2*pi*1j)

# ------------------------------------------------------------------------------
# Collection Generators
# ------------------------------------------------------------------------------

class CollectionGenerator(PayCheckGenerator):
    def __init__(self, t_def):
        PayCheckGenerator.__init__(self)
        self.inner = PayCheckGenerator.get(t_def)
    
    def __next__(self):
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
    bool:    BooleanGenerator,
    float:   FloatGenerator,
    complex: ComplexGenerator,
  }

if sys.version_info[0] < 3:
    scalar_generators[unicode] = UnicodeGenerator

container_generators = {
    list:    ListGenerator,
    dict:    DictGenerator,
    set:     SetGenerator,
    tuple:   TupleGenerator,
  }

# ------------------------------------------------------------------------------
# List of exports
# ------------------------------------------------------------------------------

__all__ = [
    'MIN_INT',
    'MAX_INT',
    'LIST_LEN',
    'PayCheckException',
    'UnknownTypeException',
    'IncompleteTypeException',
    'PayCheckGenerator',
    'StringGenerator',
    'IntGenerator',
    'irange',
    'BooleanGenerator',
    'UniformFloatGenerator',
    'frange',
    'unit_interval_float',
    'NonNegativeFloatGenerator',
    'non_negative_float',
    'PositiveFloatGenerator',
    'positive_float',
    'FloatGenerator',
    'ComplexGenerator',
    'CollectionGenerator',
    'ListGenerator',
    'SetGenerator',
    'DictGenerator',
    'TupleGenerator',
    'scalar_generators',
    'container_generators',
]

if sys.version_info[0] < 3:
    __all__.append('UnicodeGenerator')
