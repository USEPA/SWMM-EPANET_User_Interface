import unittest
from core.swmm.options import dates
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match


class OptionsDatesTest(unittest.TestCase):
    """Test OPTIONS: Dates"""

    def setUp(self):
        self.my_options = dates.Dates()

    def runTest(self):
        """Test Dates portion in OPTIONS"""
        name = self.my_options.SECTION_NAME
        assert name == "[OPTIONS]"

        expected_text = "[OPTIONS]\n" + \
                        " END_TIME           	24:00\n" + \
                        " END_DATE           	1/1/2002\n" + \
                        " SWEEP_END          	12/31\n" + \
                        " START_TIME         	0:00\n" + \
                        " DRY_DAYS           	0\n" + \
                        " REPORT_START_TIME  	0:00\n" + \
                        " START_DATE         	1/1/2002\n" + \
                        " SWEEP_START        	1/1\n" + \
                        " REPORT_START_DATE  	1/1/2002"

        assert match(SectionWriter.as_text(self.my_options), expected_text)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
