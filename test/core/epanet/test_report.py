import unittest
from core.epanet.options.options import Options
from core.epanet.options import report


class SimpleReportTest(unittest.TestCase):
    """Test Report section"""
    def test_simple(self):
        """Test simple report options"""
        self.my_report = report.ReportOptions()
        self.my_report.pagesize = 64
        name = self.my_report.SECTION_NAME
        assert name == "[REPORT]"
        expected_text = "[REPORT]\n" + \
                        " Status             	NO\n" + \
                        " Energy             	NO\n" + \
                        " Page               \t64\n" + \
                        " Summary            	YES"
        assert self.my_report.matches(expected_text)

    def test_page(self):
        """Test simple report options with small variation in page setup"""
        self.my_report = report.ReportOptions()
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

    def test_all(self):
        """Test all report options based on manual P162"""
        self.my_report = report.ReportOptions()
        name = self.my_report.SECTION_NAME
        assert name == "[REPORT]"
        test_text = "[REPORT]\n" + \
                    "Status NO\n" + \
                    "Energy NO\n" + \
                    "Summary NO\n" + \
                    "NODES N1 N2 N3 N17\n" + \
                    "LINKS ALL\n" \
                    "FLOW YES\n" + \
                    "VELOCITY PRECISION 4\n" \
                    "F-FACTOR PRECISION 4\n " \
                    "VELOCITY ABOVE 3.0"
        self.my_report.set_text(test_text)
        actual_text = self.my_report.get_text()
        assert self.my_report.matches(test_text)

