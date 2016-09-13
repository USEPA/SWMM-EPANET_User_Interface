import unittest
from core.swmm.inp_reader_sections import TransectReader, TransectsReader
from core.swmm.inp_writer_sections import TransectWriter, TransectsWriter
from core.swmm.hydraulics.link import Transect, Transects
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class SimpleTransectTest(unittest.TestCase):
    """Test TRANSECTS section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_one_transect(self):
        """Test one transect from Example-7-final"""
        test_text ="NC\t0.016\t0.016\t0.016\n" \
                   "X1\tFull_Street\t7\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\n" \
                   "GR\t1.3\t-40\t0.5\t-20\t0\t-20\t0.8\t0\t0\t20\n" \
                   "GR\t0.5\t20\t1.3\t40"
        my_options = TransectReader.read(test_text)
        actual_text = TransectWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_transects(self):
        """Test transects:Example-7-final inp
        # -- Output does not match input, only one transect was kept and GRs gets combined"""
        source_text = "[TRANSECTS]\n" \
                      "NC 0.015    0.015    0.015\n" \
                      "X1 Full_Street       7        0.0      0.0      0.0      0.0      0.0      0.0      0.0\n" \
                      "GR 1.3      -40      0.5      -20      0        -20      0.8      0        0        20\n" \
                      "GR 0.5      20       1.3      40\n" \
                      "NC 0.016    0.016    0.016\n" \
                      "X1 Half_Street       5        0.0      0.0      0.0      0.0      0.0      0.0      0.0\n" \
                      "GR 1.3      -40      0.5      -20      0        -20      0.8      0        1.3      0"
        section_from_text = self.project_reader.read_transects.read(source_text)
        actual_text = self.project_writer.write_transects.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match(actual_text, source_text), msg)

    def test_transect_section(self):
        """Test transects: using Project
        # -- Output does not match input, only one transect was kept and GRs gets combined"""
        source_text = r"""[TRANSECTS]
        NC 0.015    0.015    0.015
        X1 Full_Street       7        0.0      0.0      0.0      0.0      0.0      0.0      0.0
        GR 1.3      -40      0.5      -20      0        -20      0.8      0        0        20
        GR 0.5      20       1.3      40
        NC 0.016    0.016    0.016
        X1 Half_Street       5        0.0      0.0      0.0      0.0      0.0      0.0      0.0
        GR 1.3      -40      0.5      -20      0        -20      0.8      0        1.3      0
        """
        section_from_text = self.project_reader.read_transects.read(source_text)
        actual_text = self.project_writer.write_transects.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match(actual_text, source_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()