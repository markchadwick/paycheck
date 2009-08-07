from distutils.cmd import Command
class test(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import tests
        tests.run_tests()

from distutils.core import setup
setup(name = 'paycheck',
      version ='0.4.2',
      description ='A Python QuickCheck implementation',
      author ='Mark Chadwick',
      author_email ='mark.chadwick@gmail.com',
      url='http://github.com/markchadwick/paycheck/tree/master',
      packages = ['paycheck'],
      cmdclass = {"test" : test}
      )
      
