import unittest
from paycheck.generator import *

class TestTypes(unittest.TestCase):
    def test_get_int(self):
        self.assertEquals(
                    IntGenerator,
                    PayCheckGenerator._generator_for_type(int))
        
    def test_get_string(self):
        self.assertEquals(
                    StringGenerator,
                    PayCheckGenerator._generator_for_type(str))
    
    def test_get_unicode(self):
        self.assertEquals(
                    UnicodeGenerator,
                    PayCheckGenerator._generator_for_type(unicode))
    
    def test_get_boolean(self):
        self.assertEquals(
                    BooleanGenerator,
                    PayCheckGenerator._generator_for_type(bool))
    
    def test_get_list(self):
        self.assertEquals(
                    ListGenerator,
                    PayCheckGenerator._generator_for_type(list))

    def test_get_dict(self):
        self.assertEquals(
                    DictGenerator,
                    PayCheckGenerator._generator_for_type(dict))
    
    def test_get_float(self):
        self.assertEquals(
                    FloatGenerator,
                    PayCheckGenerator._generator_for_type(float))
        
    def test_get_set(self):
        self.assertEquals(
                    SetGenerator,
                    PayCheckGenerator._generator_for_type(set))
    
    def test_get_unknown_type_throws_exception(self):
        getter = lambda: PayCheckGenerator._generator_for_type(tuple)
        self.assertRaises(UnknownTypeException, getter)
        
    def test_bad_object_throws_exception(self):
        getter = lambda: PayCheckGenerator._generator_for_type("what?")
        self.assertRaises(AssertionError, getter)
        
    def test_get_list_of_type(self):
        generator = PayCheckGenerator.get((list, int))
        self.assertTrue(isinstance(generator, ListGenerator))
        self.assertTrue(isinstance(generator.inner, IntGenerator))
        
    def test_get_nested_list_of_type(self):
        generator = PayCheckGenerator.get((list, (list, int)))
        self.assertTrue(isinstance(generator, ListGenerator))
        self.assertTrue(isinstance(generator.inner, ListGenerator))
        self.assertTrue(isinstance(generator.inner.inner, IntGenerator))
    
    def test_malformatted_list(self):
        getter = lambda: PayCheckGenerator.get(list)
        self.assertRaises(UnknownTypeException, getter)
    
    def test_dict_of_str_int(self):
        generator = PayCheckGenerator.get((dict, (str, int)))
        self.assertTrue(isinstance(generator, DictGenerator))
        self.assertTrue(isinstance(generator.k_inner, StringGenerator))
        self.assertTrue(isinstance(generator.v_inner, IntGenerator))