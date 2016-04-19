from core.swmm.hydraulics.node import DryWeatherInflow
import unittest


class SingleDWITest(unittest.TestCase):

    def setUp(self):

        self.my_options = DryWeatherInflow()

    def runTest(self):

        # Test example 8
        test_text = r"""J1               FLOW             0.008 """
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        # Test example 3
        test_text = r"""KRO3001          FLOW             1          "" "" "DWF" "" "" "" """""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)


        pass

class MultiDWIsTest(unittest.TestCase):

    def setUp(self):

        self.my_options = DryWeatherInflow()

    def runTest(self):

        #Example 3
        test_text = r"""
[DWF]
;;                                  Average    Time
;;Node             Parameter        Value      Patterns
;;-----------------------------------------------------
  KRO3001          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO6015          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO6016          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO6017          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1002          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1003          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1004          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1005          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1006          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1007          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1008          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1009          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1010          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1012          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1013          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1015          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO2001          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4004          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4008          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4009          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4010          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4011          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4012          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4013          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4014          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4015          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4017          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4018          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4019          FLOW             1          "" "" "DWF" "" "" "" ""
  SU1              FLOW             1          "" "" "DWF" "" "" "" ""
        """
        # Example 8
        test_text = """[DWF]
;;                                Average    Time
;;Node           Parameter        Value      Patterns
;;-------------- ---------------- ---------- ----------
J1               FLOW             0.008
J2a              FLOW             0.01
J12              FLOW             0.0125
J13              FLOW             0.0123
Aux3             FLOW             0.004     """
        # --Test set_text


        pass