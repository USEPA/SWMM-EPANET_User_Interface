import unittest
from core.inputfile import Section
from core.swmm.project import Project
from core.swmm.curves import Curve, CurveType


class SimpleCurveTest(unittest.TestCase):
    """Test CURVERS section"""

    def test_storage_curve(self):
        """Test one set of Storage curve (SWMM 5.1 manual Page334)"""
        test_text = "AC1 STORAGE 0 1000 2 2000 4 3500 6 4200 8 5000"
        curve1 = Curve()
        curve1.set_text(test_text)
        temp_curve = Curve()
        temp_curve.set_text(curve1.get_text())
        for curve in (curve1, temp_curve):
            assert curve.curve_id == 'AC1'
            assert curve.curve_type == CurveType.STORAGE
            assert curve.curve_xy == [('0', '1000'), ('2', '2000'), ('4', '3500'), ('6', '4200'), ('8', '5000')]

    def test_pump_curve(self):
        """Test one set of Type 1 Pump curve (SWMM 5.1 manual Page334)"""
        test_text = "PC1 PUMP1\nPC1 100 5 300 10 500 20"
        curve = Curve()
        curve.set_text(test_text)
        temp_curve = Curve()
        temp_curve.set_text(curve.get_text())
        for curve in (curve, temp_curve):
            assert curve.curve_id == 'PC1'
            assert curve.curve_type == CurveType.PUMP1
            assert curve.curve_xy == [('100', '5'), ('300', '10'), ('500', '20')]

    def test_curves_section(self):  # TODO: check the match_omit method
        """Test CURVES section using Project class, Example6-Initial"""
        from_text = Project()
        # source_text = '\n'.join(self.TEST_TEXT)
        source_text = "[CURVES]\n" \
                      ";;Name           Type       X-Value    Y-Value\n" \
                      ";;-------------- ---------- ---------- ----------\n" \
                      "SU2              Storage    0          10368\n" \
                      "SU2                         2.2        14512\n" \
                      "SU2                         2.3        32000\n" \
                      "SU2                         6          50000"
        from_text.set_text(source_text)
        project_section = from_text.curves
        assert Section.match_omit(project_section.get_text(), source_text, " \t-;\n")