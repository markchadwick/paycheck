import unittest
from pycheck import with_checker

class TestTypes(unittest.TestCase):

    @with_checker(str)
    def test_string(self, s):
        self.assertTrue(isinstance(s, str))

    @with_checker(int)
    def test_int(self, i):
        self.assertTrue(isinstance(i, int))

    @with_checker(unicode)
    def test_unicode(self, u):
        self.assertTrue(isinstance(u, unicode) or
                        isinstance(u, str))

    @with_checker(bool)
    def test_boolean(self, b):
        self.assertEquals(b, b == True)

    @with_checker((list, int))
    def test_list_of_ints(self, list_of_ints):
        for i in list_of_ints:
            self.assertTrue(isinstance(i, int))

    @with_checker(str, (list, (list, bool)))
    def test_nested_types(self, s, list_of_lists_of_bools):
        self.assertTrue(isinstance(s, str))
        self.assertTrue(isinstance(list_of_lists_of_bools, list))
        
        for list_of_bools in list_of_lists_of_bools:
            self.assertTrue(isinstance(list_of_bools, list))
            for b in list_of_bools:
                self.assertTrue(isinstance(b, bool))

if __name__ == '__main__':
    unittest.main()
