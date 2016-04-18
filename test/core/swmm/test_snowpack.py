from core.swmm.hydrology.snowpack import SnowPack
import unittest


class SnowPackTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = SnowPack()

    def runTest(self):
        # Test snow parameters from Example 1h, examined according to SWMM 5.1 manual
        # Modified on test purposes
        # This test passed for an individual snowpack parameter set
        # Case 1: test all snowpack surface types
        test_snowpack_all = r"""
;;Name           Surface    Parameters
;;-------------- ---------- ----------
s                PLOWABLE   0.001      0.001      32.0       0.10       0.00       0.00       0.0
s                IMPERVIOUS 0.001      0.001      32.0       0.10       0.00       0.00       0.00
s                PERVIOUS   0.001      0.001      32.0       0.10       0.00       0.00       0.00
s                REMOVAL    1.0        0.0        0.0        0.0        0.0        0.0        w
        """
        # --Test set_text
        self.my_options.set_text(test_snowpack_all)
        # --Test get_text through matches
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_snowpack_all)
        pass

        # Case 2: test only one type
        test_snowpack_removal = r"""
        ;;Name           Surface    Parameters
        ;;-------------- ---------- ----------
        s                REMOVAL    1.0        0.0        0.0        0.0        0.0        0.0        w
                """
        # --Test set_text
        self.my_options.set_text(test_snowpack_removal)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_snowpack_removal)
        pass

        # Test snowpacks not yet completed.
        test_snowpacks = r"""
[SNOWPACKS]
;;Name           Surface    Parameters
;;-------------- ---------- ----------
sno              PLOWABLE   0.001      0.001      32.0       0.10       0.00       0.00       0.0
sno              IMPERVIOUS 0.001      0.001      32.0       0.10       0.00       0.00       0.00
sno              PERVIOUS   0.001      0.001      32.0       0.10       0.00       0.00       0.00
sno              REMOVAL    1.0        0.0        0.0        0.0        0.0        0.0
s                PLOWABLE   0.001      0.001      32.0       0.10       0.00       0.00       0.0
s                IMPERVIOUS 0.001      0.001      32.0       0.10       0.00       0.00       0.00
s                PERVIOUS   0.001      0.001      32.0       0.10       0.00       0.00       0.00
s                REMOVAL    1.0        0.0        0.0        0.0        0.0        0.0        w
        """