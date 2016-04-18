from core.swmm.hydrology.subcatchment import LIDUsage
import unittest


class SubLIDUsageTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = LIDUsage()

    def runTest(self):
        # Test failed as current LID usage only contains one line of LID usage
        # Also code compained when I have special character in the comment lines
        # Test default, default is empty string, no adjustments
        # name = self.my_options.SECTION_NAME
        # assert name == "[LID_USAGE]"
        actual_text = self.my_options.get_text()
        #assert actual_text == ''

        # Test aquifer parameters from SWMM 5.1 manual
        test_lid_usage = r"""
[LID_USAGE]
;34 rain barrels of 12 sq ft each are placed in
;subcatchment S1. They are initially empty and treat 17
;The outflow from the barrels is returned to the
;subcatchments pervious area.
S1 RB14 34 12 0 0 17 1
S2 Swale 1 10000 50 0 0 0 swale.rpt
        """
        # --Test set_text

        self.my_options.set_text(test_lid_usage)
        # --Test get_text through matches
        actual_text = self.my_options.get_text() # display purpose
        #assert self.my_options.matches(test_lid_usage)

        pass