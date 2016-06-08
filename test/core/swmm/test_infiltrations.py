import unittest
from core.inputfile import Section
from core.swmm.project import Project
from core.swmm.hydrology.subcatchment import HortonInfiltration, GreenAmptInfiltration,CurveNumberInfiltration


class InfiltrationTest(unittest.TestCase):
    """Test INFILTRATION section"""


    def test_horton(self):
        """Test Horton infiltration created based on SWMM 5.1 manual"""
        self.my_options = HortonInfiltration()
        test_text = "S1      0.35       0.25       4.14       0.50     0.0"
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

    def test_greenampt(self):
        """Test GreenAmpt infiltration created based on SWMM 5.1 manual"""
        self.my_options = GreenAmptInfiltration()
        test_text = "S1     3.5        0.2        0.2"
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

    def test_curvenumber(self):
        """Test Curver number infiltration created based on SWMM 5.1 manual"""
        self.my_options = CurveNumberInfiltration()
        test_text = "S1    3.5        0.2        2"
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

    def test_horton_infiltration_section(self):
        """Test INFILTRATION section Horton type"""
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
        from_text = Project()
        from_text.set_text(test_text)
        # from_text.infiltration.set_text('HORTON')
        project_section = from_text.infiltration
        actual_text = project_section.get_text()
        assert project_section.matches(test_text)
        # assert Section.match_omit(actual_text, test_text, " \t-;\n")

    def test_greenampt_infiltration_section(self):
        """Test INFILTRATION section Example 4a Green Ampt type"""
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
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.infiltration
        actual_text = project_section.get_text()
        assert project_section.matches(test_text)
        # assert Section.match_omit(project_section.get_text(), test_text, " \t-;\n")

    def test_curvenumber_infiltration_section(self):
        """Test INFILTRATION section curve_number type"""
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
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.infiltration
        actual_text = project_section.get_text()
        assert project_section.matches(test_text)
        # assert Section.match_omit(project_section.get_text(), test_text, " \t-;\n")
