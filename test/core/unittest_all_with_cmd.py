##  This section is needed to run coverage from the command line
## >> Run coverage from command line, navigate to test_all.py
## >> coverage unittest_all_with_cmd.py
## >> coverage report >> Report_coverage_unittest.txt
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

my_suite = unittest.TestSuite()
my_suite.addTests(test.core.epanet.test_all.my_suite)
my_suite.addTests(test.core.swmm.test_all.my_suite)

if __name__ == "__main__":
    # execute only if run as a script
    report_filename = "test_results_core.html"
    fp = open(report_filename, 'wb')
    runner = test.HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title='SWMM-EPANET Core Test Report',
        description='Unit test results')

    runner.run(my_suite)
    fp.close()

    # Open unit_test reports
    try:
        webbrowser.open_new_tab(report_filename)
    except:
        print("Test results written to " + report_filename)