from core.swmm.hydraulics.node import Divider
import unittest


class SingleDividerTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Divider()

    def runTest(self):

        # Test junction will all parameters
        test_text = r""" 10   0          *    CUTOFF     0          0          0"""

        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        pass

class MultiDividersTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Divider()

    def runTest(self):

        test_text = r"""
[DIVIDERS]
;;Name           Elevation  Diverted Link    Type       Parameters
;;-------------- ---------- ---------------- ---------- ----------
10               0          *                CUTOFF     0          0          0
        """
        # --Test set_text


        pass