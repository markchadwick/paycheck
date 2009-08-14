import unittest
from paycheck import with_checker

class TestUsage(unittest.TestCase):

    @with_checker()
    def test_defaults(self, i=int, f=float):
        self.assertTrue(isinstance(i, int))
        self.assertTrue(isinstance(f, float))

    @with_checker(int)
    def test_mixed(self, i, f=float):
        self.assertTrue(isinstance(i, int))
        self.assertTrue(isinstance(f, float))

    @with_checker
    def test_without_parentheses(self, i=int, f=float):
        self.assertTrue(isinstance(i, int))
        self.assertTrue(isinstance(f, float))

tests = [TestUsage]

if __name__ == '__main__':
    unittest.main()
