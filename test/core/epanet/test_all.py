import webbrowser
import unittest
import test.HTMLTestRunner
from test.core.epanet.test_title import SimpleTitleTest
from test.core.epanet.test_options import SimpleOptionsTest
from test.core.epanet.test_quality import SimpleQualityTest
from test.core.epanet.test_reactions import SimpleReactionsTest
# from test_times import SimpleTimesTest
from test.core.epanet.test_energy import SimpleEnergyTest
from test.core.epanet.test_report import SimpleReportTest
from test.core.epanet.test_backdrop import SimpleBackdropTest
# from test_project import ProjectTest  # Changes to a individual regression test
from test.core.epanet.test_patterns import SimplePatternTest
from test.core.epanet.test_curves import SimpleCurveTest
from test.core.epanet.test_demands import SimpleDemandsTest
from test.core.epanet.test_sources import SimpleSourcesTest

my_suite = unittest.TestSuite()

# Title - MTP 1:
my_suite.addTest(SimpleTitleTest('test_bare'))
my_suite.addTest(SimpleTitleTest('test_empty'))
my_suite.addTest(SimpleTitleTest('test_one_row'))
my_suite.addTest(SimpleTitleTest('test_multi_row'))
my_suite.addTest(SimpleTitleTest('test_rt_before_title'))

# Options and reporting - MTP 1:
my_suite.addTest(SimpleOptionsTest('test_get'))
my_suite.addTest(SimpleOptionsTest('test_setget'))
# my_suite.addTest(SimpleTimesTest('test_get'))
# my_suite.addTest(SimpleTimesTest('test_no_leading_space'))
# my_suite.addTest(SimpleTimesTest('test_leading_space'))
my_suite.addTest(SimpleReportTest('test_simple'))
my_suite.addTest(SimpleReportTest('test_page'))
my_suite.addTest(SimpleReportTest('test_all'))

# Network components - MTP 3:
# junctions
# Reservoirs
# Tanks
# Pipes
# Pumps
# Valves
# Emitters

# System operation - MTP 2
my_suite.addTest(SimplePatternTest('test_pattern'))
my_suite.addTest(SimplePatternTest('test_patterns'))
my_suite.addTest(SimpleCurveTest('test_curve'))
my_suite.addTest(SimpleCurveTest('test_curves'))
my_suite.addTest(SimpleEnergyTest('test_reader_writer'))
my_suite.addTest(SimpleEnergyTest('test_writer'))
# Status - MTP 3
# Controls
# Rules
my_suite.addTest(SimpleDemandsTest())

# Water quality - MTP 2:
my_suite.addTest(SimpleQualityTest('test_get'))
my_suite.addTest(SimpleQualityTest('test_setget'))
my_suite.addTest(SimpleReactionsTest('test_get'))
my_suite.addTest(SimpleReactionsTest('test_setget'))
my_suite.addTest(SimpleSourcesTest('test_row'))
my_suite.addTest(SimpleSourcesTest('test_section'))
# Mixing - MTP 3?

# Network Map/Tags - MTP 3:
# Coordinates
# Vertices
# Labels
my_suite.addTest(SimpleBackdropTest('test_writer'))
my_suite.addTest(SimpleBackdropTest('test_reader'))
# Tags

# Project test
# my_suite.addTest(ProjectTest())


if __name__ == "__main__":
    # execute only if run as a script
    # runner = unittest.TextTestRunner()
    report_filename = "test_results_epanet.html"
    fp = open(report_filename, 'wb')
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
