from core.swmm.quality import Pollutant
import unittest


class SinglePollutantTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Pollutant()

    def runTest(self):

        # Test all options
        test_text = r""" Lead             UG/L   0.0        0.0        0          0.0        NO    TSS 0.2 0.0 0.0  """

        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        pass

class MultiPollutantsTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Pollutant()

    def runTest(self):

        test_text = r"""
[POLLUTANTS]
;;                 Mass   Rain       GW         I&I        Decay      Snow
;;Name             Units  Conc.      Conc.      Conc.      Coeff.     Only  Co-Pollutant
;;------------------------------------------------------------------------------------------
  TSS              MG/L   0.0        0.0        0          0.0        NO
  Lead             UG/L   0.0        0.0        0          0.0        NO    TSS 0.2
        """
        # --Test set_text


        pass