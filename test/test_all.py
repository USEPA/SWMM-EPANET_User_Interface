import unittest
from test_title import SimpleTitleTest
from test_patterns import SimplePatternTest


runner = unittest.TextTestRunner()

my_suite = unittest.TestSuite()
my_suite.addTest(SimpleTitleTest())
my_suite.addTest(SimplePatternTest())

runner.run(my_suite)



