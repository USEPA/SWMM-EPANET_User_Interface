from core.swmm.hydrology.subcatchment import InitialLoading
import unittest


class SingleLoadingTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = InitialLoading()

    def runTest(self):

        # Test all options
        test_text = "SB1   TSS         0.1      Lead         0.01 "
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_text)

        pass


class MultiLoadingsTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = InitialLoading()

    def runTest(self):
        test_text = r"""
[LOADINGS]
;;Subcatchment     Pollutant   Loading  Pollutant   Loading
;;----------------------------------------------------------
SB1                TSS         0.1      Lead         0.01
        """

        pass