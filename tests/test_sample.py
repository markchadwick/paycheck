import unittest
from paycheck import with_checker
from paycheck.generator import irange

class TestSample(unittest.TestCase):
    
    @with_checker(str, str)
    def test_string_concatination(self, a, b):
        self.assertTrue((a+b).endswith(b))

    @with_checker(irange(0,10))
    def test_irange_range(self,i):
        self.assertTrue(i >= 0)
        self.assertTrue(i <= 10)

tests = [TestSample]

if __name__ == '__main__':
    unittest.main()
