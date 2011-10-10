import unittest
from paycheck import with_checker
import sys

class Dummy:
    pass

class TestBasics(unittest.TestCase):
    def test_calls_method(self):
        o = Dummy()
        @with_checker(number_of_calls=10)
        def call_me():
            o.times_called += 1
        o.times_called = 0
        call_me()
        self.assertEqual(10,o.times_called)

    def test_calls_method_without_parentheses(self):
        o = Dummy()
        @with_checker
        def call_me():
            o.times_called += 1
        o.times_called = 0
        call_me()
        self.assert_(o.times_called > 0)

    def test_throws_correct_exception_upon_failure(self):
        class MyException(Exception):
            pass
        e = MyException("FAIL")
        @with_checker(number_of_calls=1)
        def call_me():
            raise e
        try:
            call_me()
            self.fail("Exception was not thrown!")
        except MyException:
            pass

tests = [TestBasics]

if __name__ == '__main__':
    unittest.main()
