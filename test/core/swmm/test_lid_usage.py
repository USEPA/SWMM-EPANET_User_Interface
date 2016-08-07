import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match
from core.swmm.hydrology.subcatchment import LIDUsage


class SimpleLIDUsageTest(unittest.TestCase):
    """Test LIDUSAGE section"""

    def test_lid_usage(self):
        """Test aquifer parameters from SWMM 5.1 manual"""
        self.my_options = LIDUsage()
        test_lid_usage = " S2 Swale 1 10000 50 0 0 0 'swale.rpt' "
        self.my_options.set_text(test_lid_usage)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_lid_usage)

    def test_lid_usage_section(self):
        """Test LIDUSAGE section through Project class
         Test failed as current LID usage only contains one line of LID usage
         Also code compained when I have special character in the comment lines"""
        test_text = r"""
[LID_USAGE]
;34 rain barrels of 12 sq ft each are placed in
;subcatchment S1. They are initially empty and treat 17
;The outflow from the barrels is returned to the
;subcatchments pervious area.
S1 RB14 34 12 0 0 17 1
S2 Swale 1 10000 50 0 0 0 swale.rpt
        """
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.lid_usage
        assert match_omit(project_section.get_text(), test_text, " \t-;\n")
