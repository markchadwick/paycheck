import paycheck
from paycheck.generator import PayCheckGenerator
from itertools import izip, islice

class with_checker(object):
    def __init__(self, *types, **settings):
        self._generators = [PayCheckGenerator.get(t) for t in types]
        self._number_of_calls = settings.get("number_of_calls",paycheck.NUM_CALLS)
    
    def __call__(self, test_func):
        generators = self._generators
        number_of_calls = self._number_of_calls
        def wrapper(self):
            for v in islice(izip(*generators),number_of_calls):
                try:
                    test_func(self, *v)
                except self.failureException:
                    raise self.failureException("Failed for input " + str(v))
        
        wrapper.__doc__ = test_func.__doc__
        wrapper.__name__ = test_func.__name__
        return wrapper
