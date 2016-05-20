import sys
import glob
import webbrowser
import unittest
import PyQt4.Qt as Qt
import PyQt4.QtGui as QtGui
import test.HTMLTestRunner
import test.ui.frmTreeViewUITest as frmTreeViewUITest


class UserInterfaceTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.file = ""

    def set_file(self, file_name):
        self.file = file_name
        # self.__name__ = file_name

    def get_file(self):
        return file

    def runTest(self):

        list_tests = []
        list_actions = []
        num_actions = []
        test_num = 0

        with open(self.file, 'r') as myfile:
            for a_line in myfile:
                # Test title line denoted with #
                if a_line.startswith('#'):
                    list_tests.append(a_line.strip(' ').replace('#','').replace('\n',''))
                    test_num = len(list_tests)
                    num_actions.append(0)

                # Individual actions within a test
                elif a_line.replace(' ','').replace('\n','').replace('\t','') != '':
                    list_actions.append(a_line)

                    # The first line must be a title
                    # if not use the file name as test name
                    # test_num increase to 1
                    if test_num == 0:
                        test_num = 1
                        list_tests.append(str(self.file))
                        num_actions.append(0)
                    num_actions[test_num-1] += 1

        # Create a tree widget
        frm = frmTreeViewUITest.frmTreeViewUITest()

        # Populate the tree list with list_tests (as parent), list_actions(as children)
        frm.set_tree(list_tests, list_actions, num_actions)

        # Execute the form
        frm.exec_()

        if not frm.OK:
            self.skipTest("User Skipped")
        else:
            failed = []

            # Evaluating the status of parents and Children
            num_tests = frm.tree.topLevelItemCount()

            for i in range(num_tests):
                test_ = frm.tree.topLevelItem(i)
                test_state = test_.checkState(0) #0-not checked, 1-checked in child, 2-all
                n_actions = test_.childCount()

                if test_state == 0:
                    failed.append('\nUI test failed: '+ str(test_.text(0)))

                elif test_state == 1:
                    failed.append('\nUI test failed: ' + str(test_.text(0)))
                    for j in range(n_actions):
                        action = test_.child(j)
                        action_state = action.checkState(0)
                        if action_state == 0:
                            failed.append('Action: '+str(action.text(0)))

            if failed:
                self.fail(str(len(failed)) + " steps failed in " + self.file + ':\n' + '\n'.join(failed))


if __name__ == "__main__":
    # execute only if run as a script
    app = QtGui.QApplication(sys.argv)

    my_suite = unittest.TestSuite()

    for test_file in glob.glob("*.txt"):
        make_test = UserInterfaceTest()
        make_test.set_file(test_file)
        my_suite.addTest(make_test)

    # test_file = 'SWMM_UI_Testing.txt'
    # make_test = UserInterfaceTest()
    # make_test.set_file(test_file)
    # my_suite.addTest(make_test)

    report_filename = "test_results_ui.html"
    fp = file(report_filename, 'wb')
    runner = test.HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title='SWMM-EPANET UI Test Report',
        description='User Interface Test Results')

    runner.run(my_suite)
    fp.close()
    try:
        webbrowser.open_new_tab(report_filename)
    except:
        print("Test results written to " + report_filename)

    sys.exit(app.exec_())

