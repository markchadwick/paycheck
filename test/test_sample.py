import unittest
from pycheck import with_checker

class TestSample(unittest.TestCase):
    @with_checker(str, str)
    def test_add_strings(self, a, b):
        self.assertTrue((a+b).endswith(b))

    @with_checker(str, int)
    def test_new_types(self, s, i):
        print '%s %i' % (s, i)

if __name__ == '__main__':
    unittest.main()