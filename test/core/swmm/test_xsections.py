import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match
from core.swmm.hydraulics.link import CrossSection
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class SimpleCrossSectionTest(unittest.TestCase):
    """Test XSECTIONS section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_geom(self):
        """Predefined shapes with Geoms only"""
        test_text = r"""W1   RECT_OPEN    2.83             1.75       0          0"""
        self.my_options = CrossSection()
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(self.my_options.matches(test_text),msg)

    def test_geom_barrel(self):
        """Predefined shapes with Geoms and Barrel only"""
        test_text = r"""C1   TRAPEZOIDAL  3                5          5          5          1"""
        self.my_options = CrossSection()
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(self.my_options.matches(test_text),msg)

    def test_geom_barrel_culvert(self):
        """Predefined shapes with Geoms, Barrel and culvert"""
        test_text = r"""Culvert      	CIRCULAR    	3            	0         	0         	0         	2         	4"""
        self.my_options = CrossSection()
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(self.my_options.matches(test_text), msg)

    def test_custom_curve(self):
        """CUSTOM with Curve only"""
        test_text = r"""W1   CUSTOM    1.0  Curve1"""
        self.my_options = CrossSection()
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(self.my_options.matches(test_text), msg)

    def test_custom_curve_barrelnum(self):
        """CUSTOM with Curve and number of barrels"""
        # -- Failed because the optional number of Barrels are not read
        test_text = r"""W1   CUSTOM    1.0  Curve1  1"""
        self.my_options = CrossSection()
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(self.my_options.matches(test_text), msg)

    def test_irregular_tsectnum(self):
        """IRREGULAR with Tsect number, example 7"""
        # -- Failed with the IRREGULAR in Example 7
        # -- However, example 7 input is not consistent with SWIM5.1 input
        test_text = r"""C_Aux1       IRREGULAR    Full_Street      3          5          5          1"""
        self.my_options = CrossSection()
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(self.my_options.matches(test_text), msg)

    def test_xsections_section(self):
        """Test XSECTIONS: example 3"""
        test_text = """[XSECTIONS]
;;Link           Shape        Geom1            Geom2      Geom3      Geom4      Barrels
;;-------------- ------------ ---------------- ---------- ---------- ---------- ----------
C1               TRAPEZOIDAL  3                5          5          5          1
C2               TRAPEZOIDAL  1                0          0.0001     25         1
C3               CIRCULAR     2.25             0          0          0          1
C4               TRAPEZOIDAL  3                5          5          5          1
C5               TRAPEZOIDAL  3                5          5          5          1
C6               TRAPEZOIDAL  3                5          5          5          1
C7               CIRCULAR     3.5              0          0          0          1
C8               TRAPEZOIDAL  3                5          5          5          1
C9               TRAPEZOIDAL  3                5          5          5          1
C10              TRAPEZOIDAL  3                5          5          5          1
C11              CIRCULAR     4.75             0          0          0          1
C_out            CIRCULAR     4.75             0          0          0          1
Or1              RECT_CLOSED  0.3              0.25       0          0
Or2              RECT_CLOSED  0.5              2          0          0
Or3              RECT_CLOSED  0.25             0.35       0          0
W1               RECT_OPEN    2.83             1.75       0          0
;;Link          	Shape       	Geom1           	Geom2     	Geom3     	Geom4     	Barrels   	Culvert
;;--------------	------------	----------------	----------	----------	----------	----------	----------
Culvert         	CIRCULAR    	3               	0         	0         	0         	2         	4
Channel         	TRAPEZOIDAL 	9               	10        	2         	2         	1
Roadway         	RECT_OPEN   	50              	200       	0         	0
"""
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.xsections
        actual_text = project_section.get_text()
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(project_section.matches(test_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
