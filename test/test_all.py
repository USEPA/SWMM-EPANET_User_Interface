import unittest
from test_title import SimpleTitleTest
from test_options import SimpleOptionsTest
from test_patterns import SimplePatternTest
from project import ProjectTest
from test_curves import SimpleCurveTest

if __name__ == "__main__":
    # execute only if run as a script
    runner = unittest.TextTestRunner()

    my_suite = unittest.TestSuite()

    # for MTP 1:
    my_suite.addTest(SimpleTitleTest())
    my_suite.addTest(SimpleOptionsTest())
    # my_suite.addTest(SimpleReactionsTest())
    # my_suite.addTest(SimpleTimesTest())
    # my_suite.addTest(SimpleEnergyTest())
    # my_suite.addTest(SimpleReportTest())
    # my_suite.addTest(SimpleBackdropTest())
    # my_suite.addTest(ProjectTest())

    # will need for later MTPs:
    my_suite.addTest(SimplePatternTest())
    # my_suite.addTest(SimpleCurveTest())

    runner.run(my_suite)



