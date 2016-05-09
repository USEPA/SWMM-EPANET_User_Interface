import webbrowser
import unittest
import test.HTMLTestRunner
from test_title import SimpleTitleTest
from test_options import SimpleOptionsTest, SimpleOptionsTest2
from test_quality import SimpleQualityTest
from test_reactions import SimpleReactionsTest
from test_times import SimpleTimesTest
from test_energy import SimpleEnergyTest
from test_report import SimpleReportTest
from test_backdrop import SimpleBackdropTest
from test_project import ProjectTest
from test_patterns import SimplePatternTest
from test_curves import SimpleCurveTest
from test_demands import SimpleDemandsTest
from test_sources import SimpleSourcesTest

my_suite = unittest.TestSuite()

# Title - MTP 1:
my_suite.addTest(SimpleTitleTest())

# Options and reporting - MTP 1:
my_suite.addTest(SimpleOptionsTest())
my_suite.addTest(SimpleOptionsTest2())
my_suite.addTest(SimpleTimesTest())
my_suite.addTest(SimpleReportTest())

# Network components - MTP 3:
# junctions
# Reservoirs
# Tanks
# Pipes
# Pumps
# Valves
# Emitters

# System operation - MTP 2
my_suite.addTest(SimplePatternTest())
my_suite.addTest(SimpleCurveTest())
my_suite.addTest(SimpleEnergyTest())
# Status - MTP 3
# Controls
# Rules
my_suite.addTest(SimpleDemandsTest())

# Water quality - MTP 2:
my_suite.addTest(SimpleQualityTest())
my_suite.addTest(SimpleReactionsTest())
my_suite.addTest(SimpleSourcesTest())
# Mixing - MTP 3?

# Network Map/Tags - MTP 3:
# Coordinates
# Vertices
# Labels
# Backdrop - MTP2?
my_suite.addTest(SimpleBackdropTest())
# Tags

# Project test
my_suite.addTest(ProjectTest())


if __name__ == "__main__":
    # execute only if run as a script
    # runner = unittest.TextTestRunner()
    report_filename = "test_results_epanet.html"
    fp = file(report_filename, 'wb')
    runner = test.HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title='EPANET Core Test Report',
        description='Unit test results')

    runner.run(my_suite)
    fp.close()
    try:
        webbrowser.open_new_tab(report_filename)
    except:
        print("Test results written to " + report_filename)
