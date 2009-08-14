import paycheck
from paycheck.generator import PayCheckGenerator

from functools import partial
from itertools import izip, izip_longest, islice, repeat
import sys
from types import FunctionType

def with_checker(*args, **keywords):
    if len(args) == 1 and isinstance(args[0],FunctionType):
        return Checker()(args[0])
    else:
        return Checker(*args, **keywords)

class Checker(object):
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
        if len(self._argument_generators) + len(self._keyword_generators) > 0:
            argument_generators = izip(*self._argument_generators)
            keyword_generators = izip(*self._keyword_generators)
            generator = islice(izip_longest(argument_generators,keyword_generators,fillvalue=()),self._number_of_calls)
        else:
            generator = repeat(((),()),self._number_of_calls)
        def wrapper(*pre_args):
            for (args,keywords) in generator:
                try:
                    test_func(*(pre_args+args), **dict(keywords))
                except Exception, e:
                    raise e.__class__("Failed for input " + str(args+keywords)), None, sys.exc_traceback
        
        wrapper.__doc__ = test_func.__doc__
        wrapper.__name__ = test_func.__name__

        return wrapper
