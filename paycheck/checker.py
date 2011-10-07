import paycheck
from paycheck.generator import PayCheckGenerator

from functools import partial
import itertools
from itertools import islice, repeat
import sys
from types import FunctionType

if sys.version_info[0] < 3:
    zip = itertools.izip
    zip_longest = itertools.izip_longest
else:
    zip_longest = itertools.zip_longest

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
        self._keyword_generators = [zip(repeat(name),PayCheckGenerator.get(t)) for (name,t) in keywords.items()]
    
    def __call__(self, test_func):
        defaults = getattr(test_func,"func_defaults",getattr(test_func,"__defaults__"))
        if defaults:
            self._argument_generators += [PayCheckGenerator.get(t) for t in defaults]
        if len(self._argument_generators) + len(self._keyword_generators) > 0:
            argument_generators = zip(*self._argument_generators)
            keyword_generators = zip(*self._keyword_generators)
            generator = islice(zip_longest(argument_generators,keyword_generators,fillvalue=()),self._number_of_calls)
        else:
            generator = repeat(((),()),self._number_of_calls)
        def wrapper(*pre_args):
            i = 0
            for (args,keywords) in generator:
                try:
                    if self._verbose:
                        sys.stderr.write("%d: %r\n" % (i, args))
                    test_func(*(pre_args+args), **dict(keywords))
                except Exception as e:
                    raise e.__class__("Failed for input %s with message '%s'" % (args+keywords,e)).with_traceback(sys.exc_traceback)
                i += 1
        
        wrapper.__doc__ = test_func.__doc__
        wrapper.__name__ = test_func.__name__

        return wrapper

__all__ = [
    'with_checker',
    'Checker',
]
