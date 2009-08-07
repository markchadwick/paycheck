import unittest
from paycheck import with_checker
from paycheck.generator import irange, non_negative_float, positive_float

class TestValues(unittest.TestCase):

    @with_checker(irange(0,10))
    def test_irange_range(self,i):
        self.assertTrue(i >= 0)
        self.assertTrue(i <= 10)

    @with_checker(non_negative_float)
    def test_non_negative_floats(self,f):
        self.assertTrue(f >= 0)

    @with_checker(positive_float)
    def test_positive_floats(self,f):
        self.assertTrue(f >= 0)

tests = [TestValues]

if __name__ == '__main__':
    unittest.main()
