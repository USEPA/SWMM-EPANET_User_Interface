from core.swmm.quality import Buildup
import unittest


class SingleBuildupTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Buildup()

    def runTest(self):

        # Test all options
        test_text = r""" Residential      TSS              SAT        50       0        2        AREA """

        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        pass

class MultiBuildupTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Buildup()

    def runTest(self):

        test_text = r"""
[BUILDUP]
;;LandUse          Pollutant        Function   Coeff1   Coeff2   Coeff3   Normalizer
;;-----------------------------------------------------------------------------------
  Residential      TSS              SAT        50       0        2        AREA
  Residential      Lead             NONE       0        0        0        AREA
  Undeveloped      TSS              SAT        100      0        3        AREA
  Undeveloped      Lead             NONE       0        0        0        AREA
        """
        # --Test set_text


        pass