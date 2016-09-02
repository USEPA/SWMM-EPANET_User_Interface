import unittest
from core.swmm.inp_reader_sections import LIDControlReader
from core.swmm.inp_writer_sections import LIDControlWriter
from core.swmm.hydrology.lidcontrol import LIDControl
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class SimpleLIDControlTest(unittest.TestCase):
    """Test LID_CONTROLS section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_lid_surface(self):
        """Test LID parameters from Example 4a, examined according to SWMM 5.1 manual
        Modified on test purposes
        This test passed for an individual LID control.
        However, a data structure for LID_CONTROLS has not yet created."""
        # Case 1: test all LID controls
        test_text = """
        Swale            VS
        Swale            SURFACE    36         0.0        0.24       1.0        5"""
        my_options = LIDControlReader.read(test_text)
        actual_text = LIDControlWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_lid_control(self):
        test_text = r"""
;;Name           Type
;;BC bio-retention cell
;;RG rain garden
;;GR green roof
;;IT infiltration trench
;;PP permeable pavement
;;RB rain barrel
;;RD rooftop disconnection
;;VS vegetative swale
;;Name           Type/Layer Parameters
;;Name           SURFACE    StorHt    VegFrac     Rough      Slope     Xslope
;;Name           SOIL       Thick     Por         FC         WP        Ksat        Kcoeff     Suct
;;Name           PAVEMENT   Thick     Vratio      FracImp    Perm      Vclog
;;Name           STORAGE    Height    Vratio      Seepage    Vclog
;;Name           DRAIN      Coeff     Expon       Offset     Delay
;;Name           DRAINMAT   Thick     Vratio      Rough
;;-------------- ---------- ----------
PorousPave       PP
PorousPave       SURFACE    0.0        0.0        0.02       2          5
PorousPave       SOIL       3          0.5        0.2        0.1        0.5        10.0       3.5
PorousPave       PAVEMENT   6          0.15       0          100        0
PorousPave       STORAGE    12         0.75       0.2        0
PorousPave       DRAIN      0          0.5        0          6
PorousPave       DRAINMAT   1          0.4        0.01
        """
        my_options = LIDControlReader.read(test_text)
        actual_text = LIDControlWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        msg += "xw09/01/2016: new comment lines in actual text"
        # self.assertTrue(match(actual_text, test_text), msg)
        self.assertTrue(match_omit(actual_text, test_text, " \t-;\n"), msg)

    def test_example4a(self):
        """Test LID parameters from Example 4a, examined according to SWMM 5.1 manual"""
        source_text = r"""
[LID_CONTROLS]
GreenRoof        BC
GreenRoof        SURFACE    0.0        0.0        0.1        1.0        5
GreenRoof        SOIL       3          0.5        0.2        0.1        0.5        10.0       3.5
GreenRoof        STORAGE    1          0.75       0          0
GreenRoof        DRAIN      1          0.5        0          6

PorousPave       PP
PorousPave       SURFACE    0.0        0.0        0.02       2          5
PorousPave       PAVEMENT   6          0.15       0          100        0
PorousPave       STORAGE    12         0.75       0.2        0
PorousPave       DRAIN      0          0.5        0          6

Planters         BC
Planters         SURFACE    6          0.0        0.0        0.0        5
Planters         SOIL       12         0.5        0.2        0.1        0.5        10.0       3.5
Planters         STORAGE    12         0.5        0.2        0
Planters         DRAIN      0          1          0.5        6

InfilTrench      IT
InfilTrench      SURFACE    0.0        0.0        0.24       0.4        5
InfilTrench      STORAGE    36         0.40       0.2        0
InfilTrench      DRAIN      0          0.5        0          6

RainBarrels      RB
RainBarrels      STORAGE    48         1          0          0
RainBarrels      DRAIN      1          0.5        0          6

Swale            VS
Swale            SURFACE    36         0.0        0.24       1.0        5"""

        section_from_text = self.project_reader.read_lid_controls.read(source_text)
        actual_text = self.project_writer.write_lid_controls.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match_omit(actual_text, source_text, " \t-;\n"), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
