import webbrowser
import unittest
from test.HTMLTestRunner import HTMLTestRunner
from test_title import SimpleTitleTest
# from test_options import SimpleOptionsTest
# from test_patterns import SimplePatternTest
from test_project import ProjectTest
from test_options_general import OptionsGeneralTest
from test_options_backdrop import OptionsBackdropTest
from test_options_dates import OptionsDatesTest
from test_options_dynamicwave import OptionsDynamicWaveTest
from test_options_interfacefiles import OptionsInterfaceFilesTest
from test_options_reporting import OptionsReportingTest
from test_options_timesteps import OptionsTimestepTest
# from test_curves import SimpleCurveTest
# from test_energy import SimpleEnergyTest
from test_aquifers import SimpleAquifersTest
from test_hydrographs import SimpleHydrographsTest
from test_evaporation import SimpleEvaporationTest

my_suite = unittest.TestSuite()

# for MTP 1:
my_suite.addTest(SimpleTitleTest())
my_suite.addTest(OptionsGeneralTest())
my_suite.addTest(OptionsDatesTest())
my_suite.addTest(OptionsTimestepTest())
my_suite.addTest(OptionsDynamicWaveTest())
my_suite.addTest(OptionsInterfaceFilesTest())
my_suite.addTest(OptionsReportingTest())
my_suite.addTest(OptionsBackdropTest())
my_suite.addTest(ProjectTest())

# will need for later MTPs:
# my_suite.addTest(SimplePatternTest())
# my_suite.addTest(SimpleCurveTest())

my_suite.addTest(SimpleAquifersTest())
my_suite.addTest(SimpleHydrographsTest())
my_suite.addTest(SimpleEvaporationTest())

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
