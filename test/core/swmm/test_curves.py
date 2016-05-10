from core.swmm.curves import Curve, CurveType
import unittest


class SingleCurveTest(unittest.TestCase):

    def runTest(self):

        # Storage curve (SWMM 5.1 manual Page334)
        # -- Failed, only the first set of values (height-area relationship) was read. "AC1 STORAGE 0 1000"
        test_text = "AC1 STORAGE 0 1000 2 2000 4 3500 6 4200 8 5000"
        curve1 = Curve()
        curve1.set_text(test_text)

        temp_curve = Curve()
        temp_curve.set_text(curve1.get_text())
        for curve in (curve1, temp_curve):
            assert curve.curve_id == 'AC1'
            assert curve.curve_type == CurveType.STORAGE
            assert curve.curve_xy == [('0', '1000'), ('2', '2000'), ('4', '3500'), ('6', '4200'), ('8', '5000')]

        # Type 1 Pump curve (SWMM 5.1 manual Page334)
        # -- Failed, only the first set of values was read "PC1 PUMP1\nPC1 100 5"
        test_text = "PC1 PUMP1\nPC1 100 5 300 10 500 20"
        curve2 = Curve()
        curve2.set_text(test_text)

        temp_curve = Curve()
        temp_curve.set_text(curve2.get_text())
        for curve in (curve2, temp_curve):
            assert curve.curve_id == 'PC1'
            assert curve.curve_type == CurveType.PUMP1
            assert curve.curve_xy == [('100', '5'), ('300', '10'), ('500', '20')]

        pass

