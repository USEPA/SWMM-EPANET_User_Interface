import unittest
from core.swmm.inp_reader_sections import CurveReader
from core.swmm.inp_writer_sections import CurveWriter
from core.swmm.curves import Curve, CurveType
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit, match_omit_nocase


class SimpleCurveTest(unittest.TestCase):
    """Test CURVERS section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_storage_curve(self):
        """Test one set of Storage curve (SWMM 5.1 manual Page334)"""
        test_text = "AC1 STORAGE 0 1000 2 2000 4 3500 6 4200 8 5000"
        curve1 = CurveReader.read(test_text)
        actual_text = CurveWriter.as_text(curve1)
        temp_curve = CurveReader.read(actual_text)
        for curve in (curve1, temp_curve):
            assert curve.name == 'AC1'
            assert curve.curve_type == CurveType.STORAGE
            assert curve.curve_xy == [('0', '1000'), ('2', '2000'), ('4', '3500'), ('6', '4200'), ('8', '5000')]

    def test_pump_curve(self):
        """Test one set of Type 1 Pump curve (SWMM 5.1 manual Page334)"""
        test_text = "PC1 PUMP1\nPC1 100 5 300 10 500 20"
        curve1 = CurveReader.read(test_text)
        actual_text = CurveWriter.as_text(curve1)
        temp_curve = CurveReader.read(actual_text)
        for curve in (curve1, temp_curve):
            assert curve.name == 'PC1'
            assert curve.curve_type == CurveType.PUMP1
            assert curve.curve_xy == [('100', '5'), ('300', '10'), ('500', '20')]

    def test_curves_section(self):  # TODO: check the match_omit method
        """Test CURVES section using Project class, Example6-Initial"""
        source_text = "[CURVES]\n" \
                      ";;Name           Type       X-Value    Y-Value\n" \
                      ";;-------------- ---------- ---------- ----------\n" \
                      "SU2              Storage    0          10368\n" \
                      "SU2                         2.2        14512\n" \
                      "SU2                         2.3        32000\n" \
                      "SU2                         6          50000"
        section_from_text = self.project_reader.read_curves.read(source_text)
        actual_text = self.project_writer.write_curves.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        msg += "\nxw09/01/2016: match_omit should omit upper and lower cases"
        self.assertTrue(match_omit_nocase(actual_text, source_text, " \t-;\n"), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()