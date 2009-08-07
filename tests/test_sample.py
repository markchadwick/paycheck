import unittest
from paycheck import with_checker
from paycheck.generator import irange

class TestSample(unittest.TestCase):
    
    @with_checker(str, str)
    def test_string_concatination(self, a, b):
        self.assertTrue((a+b).endswith(b))

tests = [TestSample]

if __name__ == '__main__':
    unittest.main()
