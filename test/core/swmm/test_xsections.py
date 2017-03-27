import unittest
from core.swmm.inp_reader_sections import CrossSectionReader
from core.swmm.inp_writer_sections import CrossSectionWriter
from core.swmm.hydraulics.link import CrossSection
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit, match_keyword_lines

class SimpleCrossSectionTest(unittest.TestCase):
    """Test XSECTIONS section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_geom(self):
        """Predefined shapes with Geoms only"""
        test_text = r"""W1   RECT_OPEN    2.83             1.75       0          0"""
        my_options = CrossSectionReader.read(test_text)
        actual_text = CrossSectionWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match_keyword_lines(test_text, actual_text,
                                            keywords_=None, skipped_keywords=None, ignore_trailing_0=True), msg)

    def test_geom_barrel(self):
        """Predefined shapes with Geoms and Barrel only"""
        test_text = r"""C1   TRAPEZOIDAL  3                5          5          5          1"""
        my_options = CrossSectionReader.read(test_text)
        actual_text = CrossSectionWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_geom_barrel_culvert(self):
        """Predefined shapes with Geoms, Barrel and culvert"""
        test_text = r"""Culvert      	CIRCULAR    	3            	0         	0         	0         	2         	4"""
        my_options = CrossSectionReader.read(test_text)
        actual_text = CrossSectionWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_custom_curve(self):
        """CUSTOM with Curve only"""
        test_text = r"""W1   CUSTOM    1.0  Curve1"""
        my_options = CrossSectionReader.read(test_text)
        actual_text = CrossSectionWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match_keyword_lines(test_text, actual_text,
                                            keywords_=None, skipped_keywords=None, ignore_trailing_0=True), msg)

    def test_custom_curve_barrelnum(self):
        """CUSTOM with Curve and number of barrels"""
        # -- Failed because the optional number of Barrels are not read
        test_text = r"""W1   CUSTOM    1.0  Curve1  1"""
        my_options = CrossSectionReader.read(test_text)
        actual_text = CrossSectionWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_irregular_tsectnum(self):
        """IRREGULAR with Tsect number, example 7"""
        # -- Failed with the IRREGULAR in Example 7
        # -- However, example 7 input is not consistent with SWIM5.1 input
        test_text = r"""C_Aux1       IRREGULAR    Full_Street      3          5          5          1"""
        my_options = CrossSectionReader.read(test_text)
        actual_text = CrossSectionWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

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
        section_from_text = self.project_reader.read_xsections.read(test_text)
        actual_text = self.project_writer.write_xsections.as_text(section_from_text)
        msg = '\nSet:\n' + test_text + '\nGet:\n' + actual_text
        # self.assertTrue(match(actual_text, source_text), msg)
        self.assertTrue(match_keyword_lines(test_text, actual_text,
                            keywords_=None, skipped_keywords=None, ignore_trailing_0=True), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
