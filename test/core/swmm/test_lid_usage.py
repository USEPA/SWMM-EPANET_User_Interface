import unittest
from core.swmm.inp_reader_sections import LIDUsageReader
from core.swmm.inp_writer_sections import LIDUsageWriter
from core.swmm.hydrology.subcatchment import LIDUsage
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class SimpleLIDUsageTest(unittest.TestCase):
    """Test LIDUSAGE section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_lid_usage(self):
        """Test aquifer parameters from SWMM 5.1 manual"""
        test_text = " S2 Swale 1 10000 50 0 0 0 'swale.rpt' * 0 "
        my_options = LIDUsageReader.read(test_text)
        actual_text = LIDUsageWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_lid_usage_section(self):
        """Test LIDUSAGE section through Project class
         Test failed as current LID usage only contains one line of LID usage
         Also code compained when I have special character in the comment lines"""
        source_text = "[LID_USAGE]\n" \
                      ";34 rain barrels of 12 sq ft each are placed in\n" \
                      ";subcatchment S1. They are initially empty and treat 17\n" \
                      ";The outflow from the barrels is returned to the\n" \
                      ";subcatchments pervious area.\n" \
                      "S1 RB14 34 12 0 0 17 1 * * 0 \n" \
                      "S2 Swale 1 10000 50 0 0 0 swale.rpt * 0 \n"
        section_from_text = self.project_reader.read_lid_usage.read(source_text)
        actual_text = self.project_writer.write_lid_usage.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match(actual_text, source_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
