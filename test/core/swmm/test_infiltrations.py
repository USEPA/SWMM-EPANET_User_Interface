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
from core.swmm.swmm_project import SwmmProject

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
        """Test INFILTRATION section Horton type, tested reader only, not writer"""
        source_text = "[INFILTRATION]\n" \
                      ";;Subcatchment     MaxRate    MinRate    Decay      DryTime\n" \
                      ";;-----------------------------------------------------------------------\n" \
                      "  1                0.35       0.25       4.14       0.50\n" \
                      "  2                0.7        0.3        4.14       0.50\n" \
                      "  3                0.7        0.3        4.14       0.50\n" \
                      "  4                0.7        0.3        4.14       0.50\n" \
                      "  5                0.7        0.3        4.14       0.50\n" \
                      "  6                0.7        0.3        4.14       0.50\n" \
                      "  7                0.7        0.3        4.14       0.50\n" \
                      "  8                0.7        0.3        4.14       0.50"
        section_name = "[INFILTRATION]"
        my_project = SwmmProject()
        my_project.options.infiltration = "HORTON"
        self.project_reader.read_section(my_project, section_name, source_text)
        text_rows = source_text.split("\n")
        i = 0
        for t in text_rows:
            if t.lstrip()[0] == "[" or t.lstrip()[0] == ";":
                pass
            else:
                itm = my_project.infiltration.value[i]
                i += 1
                assert isinstance(itm, HortonInfiltration)
                columns = t.split()
                assert itm.subcatchment == columns[0]
                assert itm.max_rate == columns[1]
                assert itm.min_rate == columns[2]
                assert itm.decay == columns [3]
                assert itm.dry_time == columns[4]
         #      assert itm.max_volume == columns[5]  #MaxInfil
        # actual_text = self.project_writer.as_text(my_project)
        # msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        # self.assertTrue(match(actual_text, source_text), msg)

    def test_greenampt_infiltration_section(self):
        """Test INFILTRATION section Example 4a Green Ampt type, tested reader only, not writer"""
        source_text ="[INFILTRATION]\n" \
                     ";;Subcatchment   Suction    Ksat       IMD\n" \
                     ";;-------------- ---------- ---------- ----------\n" \
                     "S1               3.5        0.2        0.2\n" \
                     "S2               3.5        0.2        0.2\n" \
                     "S3               3.5        0.2        0.2\n" \
                     "S4               3.5        0.2        0.2\n" \
                     "S5               3.5        0.2        0.2\n" \
                     "S6               3.5        0.2        0.2\n" \
                     "Swale3           3.5        0.2        0.2\n" \
                     "Swale4           3.5        0.2        0.2\n" \
                     "Swale6           3.5        0.2        0.2"
        section_name = "[INFILTRATION]"
        my_project = SwmmProject()
        my_project.options.infiltration = "GREEN"
        self.project_reader.read_section(my_project, section_name, source_text)
        text_rows = source_text.split("\n")
        i = 0
        for t in text_rows:
            if t.lstrip()[0] == "[" or t.lstrip()[0] == ";":
                pass
            else:
                itm = my_project.infiltration.value[i]
                i += 1
                assert isinstance(itm, GreenAmptInfiltration)
                columns = t.split()
                assert itm.subcatchment == columns[0]
                assert itm.suction == columns[1]
                assert itm.hydraulic_conductivity == columns[2]
                assert itm.initial_moisture_deficit == columns[3]
        # actual_text = self.project_writer.as_text(my_project)
        # msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        # self.assertTrue(match(actual_text, source_text), msg)

    def test_curvenumber_infiltration_section(self):
        """Test INFILTRATION section curve_number type,tested reader only, not writer"""
        source_text = "[INFILTRATION]\n" \
                      "        ;;Subcatchment   CurveNo    Ksat       DryTime\n" \
                      "        ;;-------------- ---------- ---------- ----------\n" \
                      " S1               3.5        0.2        2\n" \
                      "        S2               3.5        0.2        2\n" \
                      "        S3               3.5        0.2        2\n" \
                      "        S4               3.5        0.2        2\n" \
                      "        S5               3.5        0.2        2\n" \
                      "        S6               3.5        0.2        2\n" \
                      "        Swale3           3.5        0.2        2\n" \
                      "        Swale4           3.5        0.2        2\n" \
                      "        Swale6           3.5        0.2        2"
        section_name = "[INFILTRATION]"
        my_project = SwmmProject()
        my_project.options.infiltration = "CURVE"
        self.project_reader.read_section(my_project, section_name, source_text)
        text_rows = source_text.split("\n")
        i = 0
        for t in text_rows:
            if t.lstrip()[0] == "[" or t.lstrip()[0] == ";":
                pass
            else:
                itm = my_project.infiltration.value[i]
                i += 1
                assert isinstance(itm, CurveNumberInfiltration)
                columns = t.split()
                msg = "xw: CurveInfiltrationReader seems to have problem"
                self.assertTrue(itm.subcatchment == columns[0],msg)
                assert itm.curve_number == columns[1]
                assert itm.hydraulic_conductivity == columns[2]
                assert itm.dry_days == columns[3]
        # actual_text = self.project_writer.as_text(my_project)
        # msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        # self.assertTrue(match(actual_text, source_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
