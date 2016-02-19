import webbrowser
import unittest
from test.HTMLTestRunner import HTMLTestRunner
from test_title import SimpleTitleTest
# from test_options import SimpleOptionsTest
# from test_patterns import SimplePatternTest
from test_project import ProjectTest
from test_options_general import OptionsGeneralTest
# from test_curves import SimpleCurveTest
# from test_energy import SimpleEnergyTest

my_suite = unittest.TestSuite()

# for MTP 1:
my_suite.addTest(SimpleTitleTest())
# my_suite.addTest(SimpleOptionsTest())
# my_suite.addTest(SimpleReactionsTest())
# my_suite.addTest(SimpleTimesTest())
# my_suite.addTest(SimpleEnergyTest())
# my_suite.addTest(SimpleReportTest())
# my_suite.addTest(SimpleBackdropTest())
my_suite.addTest(ProjectTest())
my_suite.addTest(OptionsGeneralTest())

# will need for later MTPs:
# my_suite.addTest(SimplePatternTest())
# my_suite.addTest(SimpleCurveTest())

if __name__ == "__main__":
    # execute only if run as a script
    # runner = unittest.TextTestRunner()
    report_filename = "test_results_swmm.html"
    fp = file(report_filename, 'wb')
    runner = HTMLTestRunner(
        stream=fp,
        title='SWMM Core Test Report',
        description='Unit test results')

    runner.run(my_suite)
    fp.close()
    try:
        webbrowser.open_new_tab(report_filename)
    except:
        print("Test results written to " + report_filename)
