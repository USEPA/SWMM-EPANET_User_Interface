import unittest
from core.inputfile import Section
from core.swmm.project import Project
from core.swmm.quality import Pollutant


class SimplePollutantTest(unittest.TestCase):
    """Test POLLUTANTS section"""

    def test_one_pollutant(self):
        """Test one pollutant"""
        self.my_options = Pollutant()
        # Test all options
        test_text = r""" Lead             UG/L   0.0        0.0        0          0.0        NO    TSS 0.2 0.0 0.0  """

        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)
        self.my_options = Pollutant()

    def test_pollutant_section(self):
        """Test POLLUTANTS section through Project"""
        test_text = r"""
[POLLUTANTS]
;;                 Mass   Rain       GW         I&I        Decay      Snow
;;Name             Units  Conc.      Conc.      Conc.      Coeff.     Only  Co-Pollutant
;;------------------------------------------------------------------------------------------
  TSS              MG/L   0.0        0.0        0          0.0        NO
  Lead             UG/L   0.0        0.0        0          0.0        NO    TSS 0.2
        """
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.pollutants
        actual_text = project_section.get_text()
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(project_section.matches(test_text), msg)