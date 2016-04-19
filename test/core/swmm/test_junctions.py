from core.swmm.hydraulics.node import Junction
import unittest


class SingleJunctionTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Junction()

    def runTest(self):

        # Test junction will all parameters
        test_junction = r""" J1 2.0 0.1 0.2 0.3 0.4"""

        # --Test set_text
        self.my_options.set_text(test_junction)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_junction)

        # Test junction will all parameters
        test_junction = r""" J1 2.0 """

        # --Test set_text
        self.my_options.set_text(test_junction)
        # --Test get_text through matches
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_junction)

        pass

class MultiJunctionsTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Junction()

    def runTest(self):

        test_text = r"""
[JUNCTIONS]
;;               Invert     Max.       Init.      Surcharge  Ponded
;;Name           Elev.      Depth      Depth      Depth      Area
;;-------------- ---------- ---------- ---------- ---------- ----------
J1               4973       0          0          0          0
J2               4969       0          0          0          0
J3               4973       0          0          0          0
J4               4971       0          0          0          0
J5               4969.8     0          0          0          0
J6               4969       0          0          0          0
J7               4971.5     0          0          0          0
J8               4966.5     0          0          0          0
J9               4964.8     0          0          0          0
J10              4963.8     0          0          0          0
J11              4963       0          0          0          0
J12              4973.8     0          0          0          0
J13              4970.7     0          0          0          0
J14              4972.9     0          0          0          0
J15              4974.5     0          0          0          0
J16              4973.5     0          0          0          0
J17              4973.5     0          0          0          0
        """
        # --Test set_text


        pass