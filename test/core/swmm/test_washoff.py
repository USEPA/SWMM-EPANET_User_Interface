from core.swmm.quality import Washoff
import unittest


class SingleWashoffTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Washoff()

    def runTest(self):

        # Test all options
        test_text = r""" Residential      TSS              EXP        0.1      1        0        0  """

        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        pass

class MultiWashoffTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Washoff()

    def runTest(self):

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
        # --Test set_text


        pass