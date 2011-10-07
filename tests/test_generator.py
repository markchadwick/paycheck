import unittest
from paycheck.generator import *
import sys

class TestGenerator(unittest.TestCase):
    def test_get_int(self):
        self.assert_(isinstance(
                    PayCheckGenerator.get(int),
                    IntGenerator
                    ))
        
    def test_get_string(self):
        self.assert_(isinstance(
                    PayCheckGenerator.get(str),
                    StringGenerator
                    ))

    if sys.version_info[0] < 3:
        def test_get_unicode(self):
            self.assert_(isinstance(
                        PayCheckGenerator.get(unicode),
                        UnicodeGenerator
                        ))
    
    def test_get_boolean(self):
        self.assert_(isinstance(
                    PayCheckGenerator.get(bool),
                    BooleanGenerator
                    ))
    
    def test_get_float(self):
        self.assert_(isinstance(
                    PayCheckGenerator.get(float),
                    FloatGenerator
                    ))
    
    def test_get_unknown_type_throws_exception(self):
        getter = lambda: PayCheckGenerator.get(TestGenerator)
        self.assertRaises(UnknownTypeException, getter)
        
    def test_bad_object_throws_exception(self):
        getter = lambda: PayCheckGenerator.get("what?")
        self.assertRaises(UnknownTypeException, getter)
        
    def test_get_list_of_type(self):
        generator = PayCheckGenerator.get([int])
        self.assertTrue(isinstance(generator, ListGenerator))
        self.assertTrue(isinstance(generator.inner, IntGenerator))
        
    def test_get_nested_list_of_type(self):
        generator = PayCheckGenerator.get([[int]])
        self.assertTrue(isinstance(generator, ListGenerator))
        self.assertTrue(isinstance(generator.inner, ListGenerator))
        self.assertTrue(isinstance(generator.inner.inner, IntGenerator))
    
    def test_empty_list(self):
        getter = lambda: PayCheckGenerator.get([])
        self.assertRaises(IncompleteTypeException, getter)    

    def test_empty_dict(self):
        getter = lambda: PayCheckGenerator.get({})
        self.assertRaises(IncompleteTypeException, getter)
    
    def test_dict_of_str_int(self):
        generator = PayCheckGenerator.get({str:int})
        self.assertTrue(isinstance(generator, DictGenerator))
        self.assertTrue(isinstance(generator.inner, TupleGenerator))
        self.assertTrue(isinstance(generator.inner.generators[0], StringGenerator))
        self.assertTrue(isinstance(generator.inner.generators[1], IntGenerator))

tests = [TestGenerator]

if __name__ == '__main__':
    unittest.main()
