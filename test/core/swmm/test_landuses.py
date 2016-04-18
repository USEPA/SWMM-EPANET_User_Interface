from core.swmm.quality import Landuse
import unittest


class SingleLanduseTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Landuse()

    def runTest(self):

        # Test all options
        test_text = r""" Residential_1    0          0          0 """

        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        pass

        # Test default
        test_text = r""" Residential_1    """

        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        pass

class MultiLandusesTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Landuse()

    def runTest(self):

        test_text = r"""
[LANDUSES]
;;               Cleaning   Fraction   Last
;;Name           Interval   Available  Cleaned
;;-------------- ---------- ---------- ----------
Residential_1    0          0          0
Residential_2    0          0          0
Commercial       0          0          0
LID              0          0          0
        """
        # --Test set_text


        pass