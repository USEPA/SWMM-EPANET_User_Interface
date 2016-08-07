import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match
from core.swmm.hydrology.subcatchment import Subcatchment


class SimpleSubcatchmentTest(unittest.TestCase):
    """Test SUBCATCHMENTS section"""

    def test_pk(self):
        """Test one set of subcatchment parameters with spack"""
        self.my_options = Subcatchment()
        test_subcatchment_all = "SUB1  RG1	OT2	5	0	140     0.05 	0 s1"
        self.my_options.set_text(test_subcatchment_all)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_subcatchment_all)


    def test_nopk(self):
        """Test one set of subcatchment parameters without spack"""
        # This should print fine
        self.my_options = Subcatchment()
        test_subcatchment_wospack = "SUB1	RG1	OT2	5	0 140	0.5	0"
        self.my_options.set_text(test_subcatchment_wospack)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_subcatchment_wospack)

    def test_missing(self):
        """Test one set of subcatchment parameters missing last two parameters Slope and Clength"""
        # This should report error
        self.my_options = Subcatchment()
        test_subcatchment_partial = "SUB1	RG1	OT2	5 0 140"
        self.my_options.set_text(test_subcatchment_partial)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_subcatchment_partial)
        # self.assertFalse(self.my_options.matches(test_subcatchment_partial))

    def test_subcatchments(self):
        """Test SUBCATCHMENTS section from Example 1"""
        test_text = """[SUBCATCHMENTS]
;;                                                   Total    Pcnt.             Pcnt.    Curb     Snow
;;Name             Raingage         Outlet           Area     Imperv   Width    Slope    Length   Pack
;;----------------------------------------------------------------------------------------------------
  1                RG1              9                10       50       500      0.01     0
  2                RG1              10               10       50       500      0.01     0
  3                RG1              13               5        50       500      0.01     0
  4                RG1              22               5        50       500      0.01     0
  5                RG1              15               15       50       500      0.01     0
  6                RG1              23               12       10       500      0.01     0
  7                RG1              19               4        10       500      0.01     0
  8                RG1              18               10       10       500      0.01     0
"""
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.subcatchments
        assert match_omit(project_section.get_text(), test_text, " \t-;\n")
