import unittest
from test.core.swmm.test_base import BastForTests
from core.swmm.inp_reader_sections import LIDUsageReader
from core.swmm.inp_writer_sections import LIDUsageWriter

class SimpleLIDUsageTest(BastForTests):
    """Test LIDUSAGE section"""

    def __init__(self):
        BastForTests.__init__(self)

    def setUp(self):
        reader = LIDUsageReader()
        writer = LIDUsageWriter()
        sreader = self.project_reader.read_lid_usage
        swriter = self.project_writer.write_lid_usage
        rows = [" S2 Swale 1 10000 50 0 0 0 'swale.rpt'"]
        sections = ["[LID_USAGE]\n" \
                      ";34 rain barrels of 12 sq ft each are placed in\n" \
                      ";subcatchment S1. They are initially empty and treat 17\n" \
                      ";The outflow from the barrels is returned to the\n" \
                      ";subcatchments pervious area.\n" \
                      "S1 RB14 34 12 0 0 17 1\n" \
                      "S2 Swale 1 10000 50 0 0 0 swale.rpt\n"]
        self.set_base(reader, writer, sreader, swriter, rows, sections)

    def runTest(self):
        my_test = SimpleLIDUsageTest()
        my_test.setUp()
        my_test.test_a_row()
        my_test.test_section()

def main():
    unittest.main()

if __name__ == "__main__":
    main()

