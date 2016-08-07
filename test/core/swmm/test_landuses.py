import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match
from core.swmm.quality import Landuse


class SimpleLanduseTest(unittest.TestCase):
    """Test LANDUSES section"""


    def test_all_opts(self):
        """Test all options of one Landuse"""
        self.my_options = Landuse()
        test_text = " Residential_1    0          0          0 "
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

    def test_default(self):
        """Test default of one Landuse"""
        self.my_options = Landuse()
        test_text = " Residential_1    "
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

    def test_landuses(self):
        """Test LANDUSES section"""

        test_text = r"""
[LANDUSES]
;;               Cleaning   Fraction   Last
;;Name           Interval   Available  Cleaned
;;-------------- ---------- ---------- ----------
Residential_1    0          0          0
Residential_2    0          0          0
Commercial       0          0          0
LID              0          0          0
        """
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.landuses
        assert match_omit(project_section.get_text(), test_text, " \t-;\n")
