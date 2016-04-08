from core.epanet.options.options import Options
from core.epanet.options import report
import unittest


class SimpleReportTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_options = Options()

    def setUp(self):

        self.my_report = report.ReportOptions()
        self.my_report.pagesize = 64

    def runTest(self):

        name = self.my_report.SECTION_NAME
        assert name == "[REPORT]"

        expected_text = "[REPORT]\n" + \
                        " Status             	NO\n" + \
                        " Energy             	NO\n" + \
                        " Page               \t64\n" + \
                        " Summary            	YES"

        assert self.my_report.matches(expected_text)
