import unittest
from core.swmm.inp_reader_sections import LanduseReader
from core.swmm.inp_writer_sections import LanduseWriter
from core.swmm.quality import Landuse
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class SimpleLanduseTest(unittest.TestCase):
    """Test LANDUSES section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_all_opts(self):
        """Test all options of one Landuse"""
        test_text = " Residential_1    0          0          0 "
        my_options = LanduseReader.read(test_text)
        actual_text = LanduseWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_default(self):
        """Test default of one Landuse"""
        test_text = " Residential_1    "
        my_options = LanduseReader.read(test_text)
        actual_text = LanduseWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_landuses(self):
        """Test LANDUSES section"""
        source_text = r"""
[LANDUSES]
;;               Cleaning   Fraction   Last
;;Name           Interval   Available  Cleaned
;;-------------- ---------- ---------- ----------
Residential_1    0          0          0
Residential_2    0          0          0
Commercial       0          0          0
LID              0          0          0
        """
        section_from_text = self.project_reader.read_landuses.read(source_text)
        actual_text = self.project_writer.write_landuses.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match_omit(actual_text, source_text, " \t-;\n"), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
