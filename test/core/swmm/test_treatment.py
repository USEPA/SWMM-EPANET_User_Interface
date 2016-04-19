from core.swmm.hydraulics.node import Treatment
import unittest


class SingleTreatmentTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Treatment()

    def runTest(self):

        # Test examples from SWMM 5.1 manual

        # BOD first order decay
        test_text = r"""Node23 BOD C = BOD * exp(-0.05*HRT) """
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        # Lead removal 20% of TSS removal
        test_text = r"""Node23 Lead R = 0.2 * R_TSS"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        pass

class MultiTreatmentTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Treatment()

    def runTest(self):

        test_text = r"""
[TREATMENT]
;;                                  Results: R or C
;;                                  R-Fraction removal
;;                                  C-efflument concentration
;;Node             Pollutant        Result = Func
;;----------------------------------------------------------------------
  Node23            BOD              C = BOD * exp(-0.05*HRT)
  Node24            Lead             R = 0.2 * R_TSS
        """
        # --Test set_text


        pass