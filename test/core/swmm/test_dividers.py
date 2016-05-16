from core.swmm.hydraulics.node import Divider
import unittest


class SingleDividerTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Divider()

    def runTest(self):

        # OVERFLOW created according to Manual
        # Name Elev DivLink OVERFLOW (Ymax Y0 Ysur Apond)
        test_text = "NODE10   0      LK1    OVERFLOW   0      0     0     0"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.name == 'NODE10'
        assert self.my_options.elevation == '0'
        assert self.my_options.diverted_link == 'LK1'
        assert self.my_options.max_depth == '0'
        assert self.my_options.initial_depth == '0'
        assert self.my_options.surcharge_depth == '0'
        assert self.my_options.ponded_area == '0'
        assert self.my_options.matches(test_text)

        # CUTOFF created according to Manual
        # Name Elev DivLink CUTOFF Qmin (Ymax Y0 Ysur Apond)
        test_text = "NODE10   0      LK1    OVERFLOW   0       0      0     0     0"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        # TABULAR created according to Manual
        # Name Elev DivLink TABULAR Dcurve (Ymax Y0 Ysur Apond)
        test_text = "NODE10   0      LK1    TABULAR   DC0       0      0     0     0"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        # WEIR created according to Manual
        # Name Elev DivLink WEIR Qmin Ht Cd (Ymax Y0 Ysur Apond)
        test_text = "NODE10   0      LK1    WEIR   0.5   2   0.7    2    0     0"
        self.my_options.set_text(test_text)
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