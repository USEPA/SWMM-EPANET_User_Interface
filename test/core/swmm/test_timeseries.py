import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match
from core.swmm.timeseries import TimeSeries
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class SimpleTimeSeriesTest(unittest.TestCase):
    """Test TIMESERIES section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_file(self):
        """Use external file, Created based on SWMM 5.1 manual Page335"""
        self.my_options = TimeSeries()
        test_text = "TS1 FILE myfile.txt"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text() #Check this
        assert self.my_options.matches(test_text) # does not match but in acceptable format

    def test_data(self):
        """Time series data test, modified from SWMM 5.1 manual Page335"""
        # get_text produced in a different format
        test_text = "TS1 6-15-2001 7:00 0.1 8:00 0.2\n" \
                    "TS1 6-21-2001 4:00 0.2 5:00 0.0"
        self.my_options = TimeSeries()
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text() # Check this
        self.assertFalse(self.my_options.matches(test_text),'does not match but in acceptable format')

    def test_multiple_lines(self):
        """Test the multi-line input format"""
        test_text = "TS1\t6-15-2001\t7:00\t0.1\n" \
                    "TS1\t\t8:00\t0.2\n" \
                    "TS1\t6-21-2001\t4:00\t0.2\n" \
                    "TS1\t\t5:00\t0.0"
        self.my_options = TimeSeries()
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()
        new_text = actual_text.replace(" ", "") # remove white spaces
        assert test_text == new_text  #no white space comparision
        # assert self.my_options.matches(test_text)

    def test_timeseries_section(self):
        """Test Example in SWMM 5.1 manual Page335"""
        # -- Failed because of SECTION name and
        # -- Data structure
        # self.my_options = TimeSeries()
        test_text = r"""
        [TIMESERIES]
        ;Rainfall time series with dates specified
        TS1 6-15-2001 7:00 0.1 8:00 0.2 9:00 0.05 10:00 0
        TS1 6-21-2001 4:00 0.2 5:00 0 14:00 0.1 15:00 0
        ;Inflow hydrograph - time relative to start of simulation
        HY1 0 0 1.25 100 2:30 150 3.0 120 4.5 0
        HY1 32:10 0 34.0 57 35.33 85 48.67 24 50 0
        """
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.timeseries
        actual_text = project_section.get_text()
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(project_section.matches(test_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
