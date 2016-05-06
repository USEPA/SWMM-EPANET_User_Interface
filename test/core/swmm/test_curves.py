from core.swmm.curves import Curve
import unittest


class SingleCurveTest(unittest.TestCase):

    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = Curve()

    def runTest(self):

        # Storage curve (SWMM 5.1 manual Page334)
        # -- Failed, only the first set of values (height-area relationship) was read. "AC1 STORAGE 0 1000"
        test_text = "AC1 STORAGE 0 1000 2 2000 4 3500 6 4200 8 5000"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()
        assert test_text == actual_text
        assert self.my_options.matches(test_text)

        # Type 1 Pump curve (SWMM 5.1 manual Page334)
        # -- Failed, only the first set of values was read "PC1 PUMP1\nPC1 100 5"
        test_text = "PC1 PUMP1\nPC1 100 5 300 10 500 20"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()
        assert test_text == actual_text
        assert self.my_options.matches(test_text)

        pass

