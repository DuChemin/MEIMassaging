import sys
import unittest

import transform_test
import unit_test
import dc_test

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unit_test.suite())
    test_suite.addTest(transform_test.suite())
    test_suite.addTest(dc_test.suite())
    return test_suite
    
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite())

