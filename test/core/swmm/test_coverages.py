from core.swmm.hydrology.subcatchment import Coverage
from core.swmm.hydrology.subcatchment import Coverages
import unittest


class SingleCoverageTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Coverage()

    def runTest(self):
        # Test aquifer parameters in Example 5
        test_text = "S2               Residential_1    27"
        self.my_options.set_text(test_text)
        assert self.my_options.subcatchment_name == 'S2'
        assert self.my_options.land_use_name == 'Residential_1'
        assert self.my_options.percent_subcatchment_area == '27'
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_text)
        pass


class MultiCoveragesTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = Coverages()

    def runTest(self):
        # Test default, default is empty string, no adjustments, Failed because
        name = self.my_options.SECTION_NAME
        assert name == "[COVERAGES]"
        actual_text = self.my_options.get_text()
        assert actual_text == ''

        # Test aquifer parameters in Example 5
        test_coverages = r"""
[COVERAGES]
;;Subcatchment   Land Use         Percent
;;-------------- ---------------- ----------
S1               Residential_1    100
S2               Residential_1    27
S2               Residential_2    73
S3               Residential_1    27
S3               Residential_2    32
S4               Residential_1    9
S4               Residential_2    30
S4               Commercial       26
S5               Commercial       98
S6               Commercial       100
        """
        # --Test set_text
        self.my_options.set_text(test_coverages)
        # --Test get_text through matches
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_coverages)

        pass