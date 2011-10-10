from distutils.cmd import Command
from distutils.core import setup

import sys
if sys.version_info >= (3, 0):
    try:
        from distutils.command.build_py import build_py_2to3 as build_py
    except ImportError:
        raise ImportError("build_py_2to3 not found in distutils - it is required for Python 3.x")
else:
    from distutils.command.build_py import build_py

class test(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import tests
        tests.run_tests()

setup(
    name = 'paycheck',
    version ='0.4.6',
    description ='A Python QuickCheck implementation',
    author ='Mark Chadwick',
    author_email ='mark.chadwick@gmail.com',
    url='http://github.com/markchadwick/paycheck/tree/master',
    packages = ['paycheck'],
    cmdclass = {"build_py": build_py, "test" : test}
)
