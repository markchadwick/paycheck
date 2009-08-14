import unittest
from paycheck import with_checker

class Dummy:
    pass

class TestBasics(unittest.TestCase):
    def test_calls_method(self):
        o = Dummy()
        @with_checker(number_of_calls=10)
        def call_me(_=int):
            o.times_called += 1
        o.times_called = 0
        call_me()
        self.assertEqual(10,o.times_called)

    def test_calls_method_without_parentheses(self):
        o = Dummy()
        @with_checker
        def call_me(_=int):
            o.times_called += 1
        o.times_called = 0
        call_me()
        self.assert_(o.times_called > 0)

tests = [TestBasics]

if __name__ == '__main__':
    unittest.main()
