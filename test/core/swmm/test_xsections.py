import unittest
from core.inputfile import Section
from core.swmm.project import Project
from core.swmm.hydraulics.link import CrossSection


class SimpleCrossSectionTest(unittest.TestCase):
    """Test XSECTIONS section"""


    def test_one_xsection(self):
        self.my_options = CrossSection()
        # Simple test examples
        # Predefined shapes with Geoms only
        test_text = r"""W1   RECT_OPEN    2.83             1.75       0          0"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        # Predefined shapes with Geoms and Barrel only
        test_text = r"""C1   TRAPEZOIDAL  3                5          5          5          1"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        # Predefined shapes with Geoms, Barrel and culvert
        test_text = r"""Culvert      	CIRCULAR    	3            	0         	0         	0         	2         	4"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        # CUSTOM with Curve only
        test_text = r"""W1   CUSTOM    1.0  Curve1"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        # CUSTOM with Curve and number of barrels
        # -- Failed because the optional number of Barrels are not read
        test_text = r"""W1   CUSTOM    1.0  Curve1  1"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        # IRREGULAR with Tsect number, example 7
        # -- Failed with the IRREGULAR in Example 7
        # -- However, example 7 input is not consistent with SWIM5.1 input

        test_text = r"""C_Aux1       IRREGULAR    Full_Street      3          5          5          1"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

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
"""
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.xsections
        assert Section.match_omit(project_section.get_text(), test_text, " \t-;\n")


        # Example 6
        test_text = """[XSECTIONS]
;;Link          	Shape       	Geom1           	Geom2     	Geom3     	Geom4     	Barrels   	Culvert
;;--------------	------------	----------------	----------	----------	----------	----------	----------
Culvert         	CIRCULAR    	3               	0         	0         	0         	2         	4
Channel         	TRAPEZOIDAL 	9               	10        	2         	2         	1
Roadway         	RECT_OPEN   	50              	200       	0         	0
"""

        # Example 6-final
        test_text = """[XSECTIONS]
;;Link           Shape        Geom1            Geom2      Geom3      Geom4      Barrels
;;-------------- ------------ ---------------- ---------- ---------- ---------- ----------
C1               TRAPEZOIDAL  3                5          5          5          1
C2               TRAPEZOIDAL  1.5              0          0.0001     25         1
C3               CIRCULAR     2.25             0          0          0          1
C4               TRAPEZOIDAL  3                5          5          5          1
C5               TRAPEZOIDAL  3                5          5          5          1
C6               TRAPEZOIDAL  3                5          5          5          1
C7               CIRCULAR     3.5              0          0          0          1
C8               TRAPEZOIDAL  3                5          5          5          1
C9               TRAPEZOIDAL  3                5          5          5          1
C10              TRAPEZOIDAL  3                5          5          5          1
C11              CIRCULAR     4.75             0          0          0          1
C12              TRAPEZOIDAL  3                5          5          5          1
C13              TRAPEZOIDAL  1.5              0          0.0001     25         1
C14              TRAPEZOIDAL  1.5              0          0.0001     25         1
C15              TRAPEZOIDAL  3                5          5          5          1
C16              TRAPEZOIDAL  3                5          5          5          1
C17              TRAPEZOIDAL  1.5              0          0.0001     25         1
C_out            CIRCULAR     4.75             0          0          0          1
Or1              RECT_CLOSED  0.16             0.25       0          0
Or2              RECT_CLOSED  0.5              2.25       0          0
W1               RECT_OPEN    2.72             1.6        0          0
"""
        # Example 7
        test_text = """[XSECTIONS]
;;Link           Shape        Geom1            Geom2      Geom3      Geom4      Barrels
;;-------------- ------------ ---------------- ---------- ---------- ---------- ----------
C2a              IRREGULAR    Half_Street      3          5          5          1
C2               IRREGULAR    Half_Street      3          5          5          1
C3               CIRCULAR     2.25             0          0          0          1
C4               TRAPEZOIDAL  3                5          5          5          1
C5               TRAPEZOIDAL  3                5          5          5          1
C6               TRAPEZOIDAL  3                5          5          5          1
C7               CIRCULAR     3.5              0          0          0          1
C8               TRAPEZOIDAL  3                5          5          5          1
C9               TRAPEZOIDAL  3                5          5          5          1
C10              TRAPEZOIDAL  3                5          5          5          1
C11              CIRCULAR     4.75             0          0          0          1
C_Aux1           IRREGULAR    Full_Street      3          5          5          1
C_Aux2           IRREGULAR    Full_Street      3          5          5          1
C_Aux1to2        IRREGULAR    Full_Street      3          5          5          1
C_Aux3           TRAPEZOIDAL  3                5          5          5          1
P1               CIRCULAR     1.33             0          0          0          1
P2               CIRCULAR     1.5              0          0          0          1
P3               CIRCULAR     1.5              0          0          0          1
P4               CIRCULAR     1.67             0          0          0          1
P5               CIRCULAR     1.83             0          0          0          1
P6               CIRCULAR     2                0          0          0          1
P7               CIRCULAR     2                0          0          0          1
P8               CIRCULAR     3.17             0          0          0          1
"""
