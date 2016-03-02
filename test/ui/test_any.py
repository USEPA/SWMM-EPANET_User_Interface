import sys
import glob
import webbrowser
import unittest
import PyQt4.Qt as Qt
import PyQt4.QtGui as QtGui
import test.HTMLTestRunner
import test.ui.frmInteractiveTest as frmInteractiveTest


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
        with open(self.file, 'r') as myfile:
            list_items=myfile.read().split("\n\n")
        frm = frmInteractiveTest.frmInteractiveTest()
        frm.set_list(list_items)

        frm.exec_()

        if not frm.OK:
            self.skipTest("User Skipped")
        else:
            failed = []
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

    for test_file in glob.glob("*.txt"):
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

