import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match
from core.swmm.hydraulics.node import Divider


class SimpleDividerTest(unittest.TestCase):
    """Test DIVIDER section"""

    def test_overflow_divider(self):
        """Test divider: OVERFLOW created according to Manual
         Name Elev DivLink OVERFLOW (Ymax Y0 Ysur Apond)
         """
        self.my_options = Divider()
        test_text = "NODE10   0      LK1    OVERFLOW   0      0     0     0"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.name == 'NODE10'
        assert self.my_options.elevation == '0'
        assert self.my_options.diverted_link == 'LK1'
        assert self.my_options.max_depth == '0'
        assert self.my_options.initial_depth == '0'
        assert self.my_options.surcharge_depth == '0'
        assert self.my_options.ponded_area == '0'
        assert self.my_options.matches(test_text)

    def test_cutoff_divider(self):
        """Test divider: CUTOFF created according to Manual
         Name Elev DivLink CUTOFF Qmin (Ymax Y0 Ysur Apond)
         """
        self.my_options = Divider()
        test_text = "NODE10   0      LK1    OVERFLOW   0       0      0     0     0"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

    def test_tabular_divider(self):
        """Test divider: TABULAR created according to Manual
        Name Elev DivLink TABULAR Dcurve (Ymax Y0 Ysur Apond)
        """
        self.my_options = Divider()
        test_text = "NODE10   0      LK1    TABULAR   DC0       0      0     0     0"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

    def test_weir_divider(self):
        """Test divider: WEIR created according to Manual
         Name Elev DivLink WEIR Qmin Ht Cd (Ymax Y0 Ysur Apond)
         """
        self.my_options = Divider()
        test_text = "NODE10   0      LK1    WEIR   0.5   2   0.7    2    0     0"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

    def test_dividers(self):
        """Test DIVIDERS section from Example-1b"""
        from_text = Project()
        source_text = "[DIVIDERS]\n" \
                    ";;Name           Elevation  Diverted Link    Type       Parameters\n" \
                    ";;-------------- ---------- ---------------- ---------- ----------\n" \
                    "10               0          *                CUTOFF     0          0          0"
        from_text.set_text(source_text)
        project_section = from_text.dividers
        assert match_omit(project_section.get_text(), source_text, " \t-;\n")
