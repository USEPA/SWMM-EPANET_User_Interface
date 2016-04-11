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

        #--Test default with formats (old--may be removed unless keep the format testing xw20160411)
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

        assert self.my_options.matches(expected_text)

        #--Test complete set_text for SWMM 5.1, consistent with defaults in 5.1
        test_all_ops = r"""[REPORT]
INPUT NO
CONTINUITY YES
FLOWSTATS YES
CONTROLS NO
SUBCATCHMENTS NONE
NODES NONE
LINKS NONE
LID NONE"""
        #--Test defaults and get_text through matches
        assert self.my_options.matches(test_all_ops)

        #--Test set_text
        self.my_options.set_text(test_all_ops)
        assert self.my_options.input == False
        assert self.my_options.continuity == True
        assert self.my_options.flow_stats == True
        assert self.my_options.controls == False
        assert self.my_options.subcatchments == ['NONE']
        assert self.my_options.nodes == ['NONE']
        assert self.my_options.links == ['NONE']
        assert self.my_options.lids == Report.EMPTY_LIST
        assert self.my_options.lids == ['NONE']

        #--Test get_text using matches, actual_text is only for displaying the text
        assert self.my_options.matches(test_all_ops)
        #--Test get_text against matches
        actual_text = self.my_options.get_text()
        assert self.my_options.matches(actual_text)

        #--Test subcatchments, nodes, links and LID lists
        #--Test complete set_text for SWMM 5.1
        test_lists = r"""[REPORT]
INPUT NO
CONTINUITY NO
FLOWSTATS NO
CONTROLS NO
SUBCATCHMENTS S1 S2 S3
NODES J1
LINKS C1
LINKS C2
LID L1 S1 L1SUB1.txt
LID L2 S1 L2SUB1.txt"""
        self.my_options.set_text(test_lists)
        assert self.my_options.input == False
        assert self.my_options.continuity == False
        assert self.my_options.flow_stats == False
        assert self.my_options.controls == False
        assert self.my_options.subcatchments == ['S1','S2','S3']
        assert self.my_options.nodes == ['J1']
        assert self.my_options.links == ['C1','C2']
        assert self.my_options.lids == ['L1', 'S1', 'L1SUB1.txt','L2','S1','L2SUB1.txt']

        #--Test get_text using matches, actual_text is only for displaying the text
        actual_text = self.my_options.get_text()
        assert self.my_options.matches(actual_text)
        #xw: input format has two lines on LID, output actual_text has only one line:
        #"LID L1 S1 L1SUB1.txt L2 S1 L2SUB1.txt"
        #Tested fine if this is desired results.

        pass
