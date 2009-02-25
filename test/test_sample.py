import unittest
from paycheck import with_checker

class TestSample(unittest.TestCase):
    
    @with_checker(str, str)
    def test_string_concatination(self, a, b):
        self.assertTrue((a+b).endswith(b))

if __name__ == '__main__':
    unittest.main()
