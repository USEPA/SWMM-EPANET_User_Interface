import unittest
from core.epanet.options import report
from core.epanet.inp_reader_sections import ReportOptionsReader
from core.epanet.inp_writer_sections import ReportOptionsWriter
from test.core.section_match import match


class SimpleReportTest(unittest.TestCase):
    """Test Report section"""
    def test_simple(self):
        """Test simple report options"""
        my_report = report.ReportOptions()
        my_report.pagesize = 64
        name = my_report.SECTION_NAME
        assert name == "[REPORT]"
        expected_text = "[REPORT]\n" + \
                        " Status             	NO\n" + \
                        " Energy             	NO\n" + \
                        " Page               \t64\n" + \
                        " Summary            	YES"
        actual_text = ReportOptionsWriter.as_text(my_report)
        msg = '\nSet:'+expected_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, expected_text), msg)

    def test_page(self):
        """Test simple report options with small variation in page setup"""
        test_text = "[REPORT]\n" + \
                    " Status             	NO\n" + \
                    " Summary            	YES\n" \
                    " Energy             	NO\n" + \
                    " Nodes            	    Node1 Node2 Node3\n" \
                    " Links             	Link1 Link2\n " \
                    " Page  64"
        my_report = ReportOptionsReader.read(test_text)
        actual_text = ReportOptionsWriter.as_text(my_report)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_all(self):
        """Test all report options based on manual P162"""
        my_report = report.ReportOptions()
        name = my_report.SECTION_NAME
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
        my_report = ReportOptionsReader.read(test_text)
        actual_text = ReportOptionsWriter.as_text(my_report)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()