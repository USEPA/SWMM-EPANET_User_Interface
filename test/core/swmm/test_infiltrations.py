import unittest
from core.swmm.inp_reader_sections import HortonInfiltrationReader,\
    GreenAmptInfiltrationReader,\
    CurveNumberInfiltrationReader
from core.swmm.inp_writer_sections import HortonInfiltrationWriter, \
    GreenAmptInfiltrationWriter, \
    CurveNumberInfiltrationWriter
from core.swmm.hydrology.subcatchment import HortonInfiltration, GreenAmptInfiltration,CurveNumberInfiltration
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class InfiltrationTest(unittest.TestCase):
    """Test INFILTRATION section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_horton(self):
        """Test Horton infiltration created based on SWMM 5.1 manual"""
        test_text = "S1      0.35       0.25       4.14       0.50     0.0"
        my_options = HortonInfiltrationReader.read(test_text)
        actual_text = HortonInfiltrationWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_greenampt(self):
        """Test GreenAmpt infiltration created based on SWMM 5.1 manual"""
        test_text = "S1     3.5        0.2        0.2"
        my_options = GreenAmptInfiltrationReader.read(test_text)
        actual_text = GreenAmptInfiltrationWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_curvenumber(self):
        """Test Curver number infiltration created based on SWMM 5.1 manual"""
        test_text = "S1    3.5        0.2        2"
        my_options = CurveNumberInfiltrationReader.read(test_text)
        actual_text = CurveNumberInfiltrationWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_horton_infiltration_section(self):
        """Test INFILTRATION section Horton type"""
        source_text = r"""
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
        section_from_text = self.project_reader.read_infiltration.read(source_text)
        actual_text = self.project_writer.write_infiltration.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match_omit(actual_text, source_text, " \t-;\n"), msg)

    def test_greenampt_infiltration_section(self):
        """Test INFILTRATION section Example 4a Green Ampt type"""
        source_text ="""[INFILTRATION]
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
        section_from_text = self.project_reader.read_infiltration.read(source_text)
        actual_text = self.project_writer.write_infiltration.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match_omit(actual_text, source_text, " \t-;\n"), msg)

    def test_curvenumber_infiltration_section(self):
        """Test INFILTRATION section curve_number type"""
        source_text = """[INFILTRATION]
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
        section_from_text = self.project_reader.read_infiltration.read(source_text)
        actual_text = self.project_writer.write_infiltration.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match_omit(actual_text, source_text, " \t-;\n"), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
