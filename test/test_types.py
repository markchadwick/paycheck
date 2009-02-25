import unittest
from paycheck import with_checker

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
    def test_get_list(self, list_of_ints):
        self.assertTrue(isinstance(list_of_ints, list))
        for i in list_of_ints:
            self.assertTrue(isinstance(i, int))

    @with_checker((set, str))
    def test_get_list(self, set_of_strs):
        self.assertTrue(isinstance(set_of_strs, set))
        for s in set_of_strs:
            self.assertTrue(isinstance(s, str))

    @with_checker((dict, (str, int)))
    def test_get_dict(self, dict_of_str_int):
        self.assertTrue(isinstance(dict_of_str_int, dict))
        for key, value in dict_of_str_int.items():
            self.assertTrue(isinstance(key, str))
            self.assertTrue(isinstance(value, int))

    @with_checker(str, (list, (list, bool)))
    def test_nested_types(self, s, list_of_lists_of_bools):
        self.assertTrue(isinstance(s, str))
        self.assertTrue(isinstance(list_of_lists_of_bools, list))
        
        for list_of_bools in list_of_lists_of_bools:
            self.assertTrue(isinstance(list_of_bools, list))
            for b in list_of_bools:
                self.assertTrue(isinstance(b, bool))

    @with_checker(int, (dict, (str, int)))
    def test_dict_of_str_key_int_values(self, i, dict_of_str_int):
        self.assertTrue(isinstance(i, int))
        self.assertTrue(isinstance(dict_of_str_int, dict))
        
        for key, value in dict_of_str_int.items():
            self.assertTrue(isinstance(key, str))
            self.assertTrue(isinstance(value, int))

    @with_checker((list, (dict, (str, int))))
    def test_list_of_dict_of_int_string(self, list_of_dict_of_int_string):
        self.assertTrue(isinstance(list_of_dict_of_int_string, list))
        
        for dict_of_int_string in list_of_dict_of_int_string:
            self.assertTrue(isinstance(dict_of_int_string, dict))

            for key, value in dict_of_int_string.items():
                self.assertTrue(isinstance(key, str))
                self.assertTrue(isinstance(value, int))

if __name__ == '__main__':
    unittest.main()
