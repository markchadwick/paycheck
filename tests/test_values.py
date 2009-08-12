import unittest
from paycheck import with_checker
from paycheck.generator import irange, non_negative_float, positive_float

class TestValues(unittest.TestCase):

    @with_checker(irange(0,10))
    def test_irange_range(self,i):
        self.assertTrue(i >= 0)
        self.assertTrue(i <= 10)

    @with_checker(irange(0,10,3))
    def test_irange_step(self,i):
        self.assertEqual(0,i%3)

    @with_checker(irange(-17,86,9))
    def test_irange_exotic(self,i):
        self.assertTrue(i >= -17)
        self.assertTrue(i <= 86)
        self.assertEqual(0,(i+17)%9)

    @with_checker(irange(0,0))
    def test_irange_tiny(self,i):
        self.assertEqual(0,i)

    @with_checker(non_negative_float)
    def test_non_negative_floats(self,f):
        self.assertTrue(f >= 0)

    @with_checker(positive_float)
    def test_positive_floats(self,f):
        self.assertTrue(f >= 0)

tests = [TestValues]

if __name__ == '__main__':
    unittest.main()
