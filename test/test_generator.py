import unittest
from pycheck.generator import *

class TestTypes(unittest.TestCase):
    def test_get_int(self):
        self.assertEquals(
                    IntGenerator,
                    PyCheckGenerator._generator_for_type(int))
        
    def test_get_string(self):
        self.assertEquals(
                    StringGenerator,
                    PyCheckGenerator._generator_for_type(str))
    
    def test_get_unicode(self):
        self.assertEquals(
                    UnicodeGenerator,
                    PyCheckGenerator._generator_for_type(unicode))
    
    def test_get_boolean(self):
        self.assertEquals(
                    BooleanGenerator,
                    PyCheckGenerator._generator_for_type(bool))
    
    def test_get_list(self):
        self.assertEquals(
                    ListGenerator,
                    PyCheckGenerator._generator_for_type(list))

    def test_get_dict(self):
        self.assertEquals(
                    DictGenerator,
                    PyCheckGenerator._generator_for_type(dict))
    
    def test_get_float(self):
        self.assertEquals(
                    FloatGenerator,
                    PyCheckGenerator._generator_for_type(float))
        
    def test_get_set(self):
        self.assertEquals(
                    SetGenerator,
                    PyCheckGenerator._generator_for_type(set))
    
    def test_get_unknown_type_throws_exception(self):
        getter = lambda: PyCheckGenerator._generator_for_type(tuple)
        self.assertRaises(UnknownTypeException, getter)
        
    def test_bad_object_throws_exception(self):
        getter = lambda: PyCheckGenerator._generator_for_type("what?")
        self.assertRaises(AssertionError, getter)
        
    def test_get_list_of_type(self):
        generator = PyCheckGenerator.get((list, int))
        self.assertTrue(isinstance(generator, ListGenerator))
        self.assertTrue(isinstance(generator.inner, IntGenerator))
        
    def test_get_nested_list_of_type(self):
        generator = PyCheckGenerator.get((list, (list, int)))
        self.assertTrue(isinstance(generator, ListGenerator))
        self.assertTrue(isinstance(generator.inner, ListGenerator))
        self.assertTrue(isinstance(generator.inner.inner, IntGenerator))
    
    def test_malformatted_list(self):
        getter = lambda: PyCheckGenerator.get(list)
        self.assertRaises(UnknownTypeException, getter)
    
    def test_dict_of_str_int(self):
        generator = PyCheckGenerator.get((dict, (str, int)))
        self.assertTrue(isinstance(generator, DictGenerator))
        self.assertTrue(isinstance(generator.k_inner, StringGenerator))
        self.assertTrue(isinstance(generator.v_inner, IntGenerator))