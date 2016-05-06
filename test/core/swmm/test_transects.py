from core.swmm.hydraulics.link import Transect, Transects
import unittest


class SingleTransectTest(unittest.TestCase):

    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = Transect()

    def runTest(self):

        # Example-7-final inp
        test_text ="NC\t0.016\t0.016\t0.016\n" \
                   "X1\tFull_Street\t7\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\n" \
                   "GR\t1.3\t-40\t0.5\t-20\t0\t-20\t0.8\t0\t0\t20\n" \
                   "GR\t0.5\t20\t1.3\t40"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text() #Check this
        new_text = actual_text.replace(" ","")
        #assert new_text == actual_text
        assert self.my_options.matches(test_text)
        pass


class MultipleTransectsTest(unittest.TestCase):

    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = Transects()

    def runTest(self):

        # Example-7-final inp
        # -- Output does not match input, only one transect was kept and GRs gets combined
        test_text = r"""[TRANSECTS]
        NC 0.015    0.015    0.015
        X1 Full_Street       7        0.0      0.0      0.0      0.0      0.0      0.0      0.0
        GR 1.3      -40      0.5      -20      0        -20      0.8      0        0        20
        GR 0.5      20       1.3      40

        NC 0.016    0.016    0.016
        X1 Half_Street       5        0.0      0.0      0.0      0.0      0.0      0.0      0.0
        GR 1.3      -40      0.5      -20      0        -20      0.8      0        1.3      0
        """
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text() #Check this
        assert self.my_options.matches(test_text) #
        pass

