import unittest
from core.swmm.options import report
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match


class SimpleReportTest(unittest.TestCase):
    """Test REPORT Section"""

    def test_reader_writer(self):
        """Test Simple ReportReader and ReportWriter"""
        test_text = "[REPORT]\n" + \
                    ";;Reporting Options\n" + \
                    " CONTINUITY         	YES\n" + \
                    " FLOWSTATS          	YES\n" + \
                    " SUBCATCHMENTS      	NONE\n" + \
                    " LINKS              	NONE\n" + \
                    " INPUT              	NO\n" + \
                    " NODES              	NONE\n" + \
                    " CONTROLS           	NO"
        my_report = ReportReader.read(test_text)
        actual_text = ReportWriter.as_text(my_report)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)
        assert my_report.input == False     # Individual inputs:
        assert my_report.continuity == True
        assert my_report.flow_stats == True
        assert my_report.controls == False
        assert my_report.subcatchments == ['NONE']
        assert my_report.nodes == ['NONE']
        assert my_report.links == ['NONE']
        assert my_report.lids == Report.EMPTY_LIST
        assert my_report.lids == ['NONE']

    def test_more(self):
        """Test Report options regarding subcatchments, nodes, links and LID lists"""
        test_text = "[REPORT]\n" \
                     "INPUT NO\n" \
                     "CONTINUITY NO\n" \
                     "FLOWSTATS NO\n" \
                     "CONTROLS NO\n" \
                     "SUBCATCHMENTS S1 S2 S3\n" \
                     "NODES J1\n" \
                     "LINKS C1\n" \
                     "LINKS C2\n" \
                     "LID L1 S1 L1SUB1.txt\n" \
                     "LID L2 S1 L2SUB1.txt"
        my_report = ReportReader.read(test_text)
        actual_text = ReportWriter.as_text(my_report)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)
        assert my_report.input == False
        assert my_report.continuity == False
        assert my_report.flow_stats == False
        assert my_report.controls == False
        assert my_report.subcatchments == ['S1','S2','S3']
        assert my_report.nodes == ['J1']
        assert my_report.links == ['C1','C2']
        assert my_report.lids == ['L1', 'S1', 'L1SUB1.txt', 'L2', 'S1', 'L2SUB1.txt']
        # assert self.my_options.matches(test_text)
        #match() did not pass because
        #input has two lines for LID
        #output put all LIDs on one line:
        #"LID L1 S1 L1SUB1.txt L2 S1 L2SUB1.txt"
        #Seems fine according to manual

def main():
    unittest.main()

if __name__ == "__main__":
    main()
