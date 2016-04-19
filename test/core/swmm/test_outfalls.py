from core.swmm.hydraulics.node import Outfall
import unittest


class SingleOutfallTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Outfall()

    def runTest(self):

        # Test junction will all parameters
        test_outfall = r""" 18      975    FREE      NO       xxx"""

        # --Test set_text
        self.my_options.set_text(test_outfall)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_outfall)


        pass

class MultiOutfallsTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Outfall()

    def runTest(self):

        test_text = r"""
[OUTFALLS]
;;Name           Elevation  Type       Stage Data       Gated    Route To
;;-------------- ---------- ---------- ---------------- -------- ----------------
18               975        FREE                        NO
[OUTFALLS]
;;Name           Elevation  Type       Stage Data       Gated    Route To
;;-------------- ---------- ---------- ---------------- -------- ----------------
18               975        FREE                        NO       xxx

        """
        # --Test set_text


        pass