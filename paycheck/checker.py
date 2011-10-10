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
    
    def __init__(self, *args, **keywords):
        self._number_of_calls = keywords.pop('number_of_calls', 100)
        self._verbose = keywords.pop('verbose', False) 
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
            i = 0
            for (args,keywords) in generator:
                try:
                    if self._verbose:
                        sys.stderr.write("%d: %r\n" % (i, args))
                    test_func(*(pre_args+args), **dict(keywords))
                except Exception, e:
                    raise e.__class__("Failed for input %s with message '%s'" % (args+keywords,e)), None, sys.exc_traceback
                i += 1
        
        wrapper.__doc__ = test_func.__doc__
        wrapper.__name__ = test_func.__name__

        return wrapper

__all__ = [
    'with_checker',
    'Checker',
]
