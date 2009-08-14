import paycheck
from paycheck.generator import PayCheckGenerator

from functools import partial
from itertools import izip, islice, repeat
import sys
from types import FunctionType

class with_checker(object):
    _argument_generators = []
    _keyword_generators = []
    _number_of_calls = 100
    def __init__(self, *args, **keywords):
        if "number_of_calls" in keywords:
            self._number_of_calls = keywords["number_of_calls"]
            del keywords["number_of_calls"]
        self._argument_generators = [PayCheckGenerator.get(t) for t in args]
        self._keyword_generators = [izip(repeat(name),PayCheckGenerator.get(t)) for (name,t) in keywords.iteritems()]
    
    def __call__(self, test_func):
        if test_func.func_defaults:
             self._argument_generators += [PayCheckGenerator.get(t) for t in test_func.func_defaults]
        argument_generators = izip(*self._argument_generators)
        keyword_generators = izip(*self._keyword_generators)
        number_of_calls = self._number_of_calls
        def wrapper(self):
            for (args,keywords) in islice(izip(argument_generators,keyword_generators),number_of_calls):
                try:
                    test_func(self, *args, **dict(keywords))
                except self.failureException:
                    raise self.failureException("Failed for input " + str(v)), None, sys.exc_traceback
        
        wrapper.__doc__ = test_func.__doc__
        wrapper.__name__ = test_func.__name__

        return wrapper
