from core.swmm.options.report import Report
from core.swmm.options import report
import unittest


class OptionsReportingTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_options = Report()

    def setUp(self):

        self.my_options = report.Report()


    def runTest(self):

        name = self.my_options.SECTION_NAME
        assert name == "[REPORT]"

        expected_text = "[REPORT]\n" + \
                        ";;Reporting Options\n" + \
                        " CONTINUITY         	YES\n" + \
                        " FLOWSTATS          	YES\n" + \
                        " SUBCATCHMENTS      	NONE\n" + \
                        " LINKS              	NONE\n" + \
                        " INPUT              	NO\n" + \
                        " NODES              	NONE\n" + \
                        " LID                	NONE\n" + \
                        " CONTROLS           	NO"

        actual_text = self.my_options.get_text() #xw: this could fail due to a unsorted dictionary problem
        assert actual_text == expected_text
