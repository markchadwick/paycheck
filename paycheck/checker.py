from paycheck.generator import PayCheckGenerator

class with_checker(object):
    def __init__(self, *types):
        self._generators = [PayCheckGenerator.get(t) for t in types]
    
    def __call__(self, test_func):
        generators = self._generators
        def wrapper(self):
            for v in zip(*generators):
                test_func(self, *v)
        
        wrapper.__doc__ = test_func.__doc__
        wrapper.__name__ = test_func.__name__
        return wrapper