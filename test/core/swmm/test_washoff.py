import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match
from core.swmm.quality import Washoff


class SimpleWashoffTest(unittest.TestCase):
    """Test WASHOFF section"""


    def test_one_washoff(self):
        """Test all options"""
        test_text = "Residential      TSS              EXP        0.1      1        0        0  "
        self.my_options = Washoff()
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

    def test_washoff_section(self):
        """Test WASHOFF section"""
        test_text = r"""
[WASHOFF]
;;                                                               Clean.   BMP
;;LandUse          Pollutant        Function   Coeff1   Coeff2   Effic.   Effic.
;;------------------------------------------------------------------------------
  Residential      TSS              EXP        0.1      1        0        0
  Residential      Lead             EMC        0        0        0        0
  Undeveloped      TSS              EXP        0.1      0.7      0        0
  Undeveloped      Lead             EMC        0        0        0        0
        """
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.washoff
        assert match_omit(project_section.get_text(), test_text, " \t-;\n")
