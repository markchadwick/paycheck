from pycheck.generator import *

GENERATORS = {
    str:  StringGenerator,
    int:  IntGenerator
}

NUM_CALLS = 100

class with_checker(object):
    def __init__(self, *types):
        for t in types:
            assert isinstance(t, type)
        self._generators = [GENERATORS[t](NUM_CALLS) for t in types]
    
    def __call__(self, test_func):
        generators = self._generators
        def wrapper(self):
            for v in zip(*generators):
                test_func(self, *v)
        
        wrapper.__doc__ = test_func.__doc__
        wrapper.__name__ = test_func.__name__
        return wrapper