##  This section is needed to run coverage from the command line
## >> Run coverage from command line, navigate to test_all.py
## >> coverage run all_unit_regress_cmd.py
## >> coverage report >> Report_coverage_all.txt
import sys
import os
current_path = os.getcwd()
project_path = os.path.split(os.path.split(current_path)[0])[0]
src_path = os.path.join(project_path, "src")
sys.path.append(project_path)
sys.path.append(src_path)
sp = sorted(sys.path)
dnames = ', '.join(sp)
print(dnames)
## ----------------------------------------------------------------------
import webbrowser
import unittest
import test.HTMLTestRunner
import test.core.epanet.test_all
import test.core.swmm.test_all
import test.core.epanet.epanetregressiontest
import test.core.swmm.swmmregressiontest

my_suite = unittest.TestSuite()
my_suite.addTests(test.core.epanet.test_all.my_suite)
my_suite.addTests(test.core.swmm.test_all.my_suite)

if __name__ == "__main__":
    # execute only if run as a script
    report_filename = "test_results_core.html"
    fp = file(report_filename, 'wb')
    runner = test.HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title='SWMM-EPANET Core Test Report',
        description='Unit test results')

    # Run unit tests
    runner.run(my_suite)

    fp.close()

    # Open unit_test reports
    try:
        webbrowser.open_new_tab(report_filename)
    except:
        print("Test results written to " + report_filename)

    # Run EPANET regression test
    reg_epanet = test.core.epanet.epanetregressiontest.EPANETRegressionTest()
    reg_epanet.runTest()

    # Run SWMM regression test
    reg_swmm = test.core.swmm.swmmregressiontest.SWMMRegressionTest()
    reg_swmm.runTest()

    # Open unit_test reports
    try:
        webbrowser.open_new_tab(report_filename)
    except:
        print("Test results written to " + report_filename)