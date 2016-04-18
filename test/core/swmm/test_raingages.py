from core.swmm.hydrology.raingage import RainGage
import unittest


class SingleRainGageTest(unittest.TestCase):

    def setUp(self):

        self.my_options = RainGage()

    def runTest(self):

        # Test aquifer parameters from SWMM 5.1 manual
        test_raingage = r"""RainGage         INTENSITY 0:05   1.0    TIMESERIES 2-yr """
        # --Test set_text
        #self.my_options.set_text(test_raingage)
        # --Test get_text through matches
        #actual_text = self.my_options.get_text() # display purpose
        #assert self.my_options.matches(test_raingage)

        pass

class MultiRainGagesTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = RainGage()

    def runTest(self):

        # Test failed as current LID usage only contains one line of LID usage
        # Also code compained when I have special character in the comment lines
        # Test default, default is empty string, no adjustments
        # name = self.my_options.SECTION_NAME
        # assert name == "[LID_USAGE]"
        #actual_text = self.my_options.get_text()
        #assert actual_text == ''

        # Test aquifer parameters from SWMM 5.1 manual
        test_text = """[RAINGAGES]
;;               Rain      Time   Snow   Data
;;Name           Type      Intrvl Catch  Source
;;-------------- --------- ------ ------ ----------
RainGage         INTENSITY 0:05   1.0    TIMESERIES 2-yr"""

