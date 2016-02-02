import unittest
from test_title import SimpleTitleTest
from test_patterns import SimplePatternTest
from test_curves import SimpleCurveTest


runner = unittest.TextTestRunner()

my_suite = unittest.TestSuite()

# for MTP 1:
my_suite.addTest(SimpleTitleTest())
# my_suite.addTest(SimpleOptionsTest())
# my_suite.addTest(SimpleReactionsTest())
# my_suite.addTest(SimpleTimesTest())
# my_suite.addTest(SimpleEnergyTest())
# my_suite.addTest(SimpleReportTest())
# my_suite.addTest(SimpleBackdropTest())

# will need for later MTPs:
my_suite.addTest(SimplePatternTest())
# my_suite.addTest(SimpleCurveTest())

runner.run(my_suite)



