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


class SimpleReportTest2(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):
        self.my_report = report.ReportOptions()

    def runTest(self):
        name = self.my_report.SECTION_NAME
        assert name == "[REPORT]"

        # Test based on P162 report
        test_text = "[REPORT]\n" + \
                    "NODES N1 N2 N3 N17\n" + \
                    "LINKS ALL\n" \
                    "FLOW YES\n" + \
                    "VELOCITY PRECISION 4\n" \
                    "F-FACTOR PRECISION 4\n " \
                    "VELOCITY ABOVE 3.0"
        self.my_report.set_text(test_text)
        actual_text = self.my_report.get_text()
        assert self.my_report.matches(test_text)

        # Test created
        test_text = "[REPORT]\n" + \
                    " Status             	NO\n" + \
                    " Summary            	YES\n" \
                    " Energy             	NO\n" + \
                    " Nodes            	    Node1 Node2 Node3\n" \
                    " Links             	Link1 Link2\n " \
                    " Page  64"
        self.my_report.set_text(test_text)
        actual_text = self.my_report.get_text()
        assert self.my_report.matches(test_text)