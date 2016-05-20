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
                    num_actions[test_num-1] += 1

        # Create a tree widget
        frm = frmTreeViewUITest.frmTreeViewUITest()

        # Populate the tree list with list_tests (as parent), list_actions(as children)
        frm.set_list(list_tests, list_actions, num_actions)

        # Execute the form
        frm.exec_()

        if not frm.OK:
            self.skipTest("User Skipped")
        else:
            failed = []

            # Evaluting the status of parents and Children
            # ---- still working xw 5/19/2016
            a = frm.tree.topLevelItemCount()
            b = frm.tree.topLevelItem(0)
            c = b.flags()
            pass

            for row in range(frm.model.rowCount()):
                item = frm.model.item(row)
                if item.checkState() != Qt.Qt.Checked:
                    failed.append(str(item.text()))

            if failed:
                self.fail(str(len(failed)) + " steps failed in " + self.file + ':\n' + '\n'.join(failed))


if __name__ == "__main__":
    # execute only if run as a script
    app = QtGui.QApplication(sys.argv)

    my_suite = unittest.TestSuite()

    test_file = "SWMM_UI_Testing.txt"
    make_test = UserInterfaceTest()
    make_test.set_file(test_file)
    my_suite.addTest(make_test)

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

