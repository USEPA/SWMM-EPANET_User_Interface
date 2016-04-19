from core.swmm.hydrology.subcatchment import HortonInfiltration, GreenAmptInfiltration,CurveNumberInfiltration
import unittest


class SingleHortonInfiltrationTest(unittest.TestCase):

    def setUp(self):

        self.my_options = HortonInfiltration()

    def runTest(self):

        # Test examples created based on SWMM 5.1 manual
        # CurveNo, Ksat, DryTime
        test_text = r"""S1      0.35       0.25       4.14       0.50     0.0"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        pass

class SingleGreenAmptInfiltrationTest(unittest.TestCase):

    def setUp(self):

        self.my_options = GreenAmptInfiltration()

    def runTest(self):

        # Test examples created based on SWMM 5.1 manual
        # CurveNo, Ksat, DryTime
        test_text = r"""S1               3.5        0.2        0.2"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        pass

class SingleCurveNumberInfiltrationTest(unittest.TestCase):

    def setUp(self):

        self.my_options = CurveNumberInfiltration()

    def runTest(self):

        # Test examples created based on SWMM 5.1 manual
        # CurveNo, Ksat, DryTime
        test_text = r"""S1               3.5        0.2        2"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        pass

class MultiInfiltrationsTest(unittest.TestCase):

    def setUp(self):

        self.my_options = HortonInfiltration()

    def runTest(self):
        # Example 1, Horton
        test_text = r"""
[INFILTRATION]
;;Subcatchment     MaxRate    MinRate    Decay      DryTime    MaxInfil
;;-----------------------------------------------------------------------
  1                0.35       0.25       4.14       0.50
  2                0.7        0.3        4.14       0.50
  3                0.7        0.3        4.14       0.50
  4                0.7        0.3        4.14       0.50
  5                0.7        0.3        4.14       0.50
  6                0.7        0.3        4.14       0.50
  7                0.7        0.3        4.14       0.50
  8                0.7        0.3        4.14       0.50
        """
        # Example 4a Green Ampt
        test_text ="""[INFILTRATION]
;;Subcatchment   Suction    Ksat       IMD
;;-------------- ---------- ---------- ----------
S1               3.5        0.2        0.2
S2               3.5        0.2        0.2
S3               3.5        0.2        0.2
S4               3.5        0.2        0.2
S5               3.5        0.2        0.2
S6               3.5        0.2        0.2
Swale3           3.5        0.2        0.2
Swale4           3.5        0.2        0.2
Swale6           3.5        0.2        0.2       """

        # Created for cuver_number
        test_text = """[INFILTRATION]
        ;;Subcatchment   CurveNo    Ksat       DryTime
        ;;-------------- ---------- ---------- ----------
        S1               3.5        0.2        2
        S2               3.5        0.2        2
        S3               3.5        0.2        2
        S4               3.5        0.2        2
        S5               3.5        0.2        2
        S6               3.5        0.2        2
        Swale3           3.5        0.2        2
        Swale4           3.5        0.2        2
        Swale6           3.5        0.2        2       """
        # --Test set_text


        pass