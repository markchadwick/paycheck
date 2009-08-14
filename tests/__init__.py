import unittest

from tests import test_generator, test_sample, test_strings, test_types, test_usage, test_values
modules = [
    test_generator,
    test_sample,
    test_strings,
    test_types,
    test_usage,
    test_values
    ]

def run_tests():
    tests = []
    for module in modules:
        for test_case in module.tests:
            tests.append(unittest.defaultTestLoader.loadTestsFromTestCase(test_case))
    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(tests))

if __name__ == "__main__":
    run_tests()
