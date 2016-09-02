import unittest
from core.swmm.inp_reader_sections import OutfallReader
from core.swmm.inp_writer_sections import OutfallWriter
from core.swmm.hydraulics.node import Outfall
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit


class SimpleOutfallTest(unittest.TestCase):
    """Test OUTFALLS section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_one_outfall(self):
        """Test one outfall will all parameters"""
        test_text = r""" 18      975    FREE      NO       xxx"""
        my_options = OutfallReader.read(test_text)
        actual_text = OutfallWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_outfall_section(self):
        """Test OUTFALLS section"""
        source_text = "[OUTFALLS]\n" \
                      ";;Name           Elevation  Type       Stage Data       Gated    Route To\n" \
                      ";;-------------- ---------- ---------- ---------------- -------- ----------------\n" \
                      "18               975        FREE                        NO\n" \
                      "18               975        FREE                        NO       xxx"
        section_from_text = self.project_reader.read_outfalls.read(source_text)
        actual_text = self.project_writer.write_outfalls.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match_omit(actual_text, source_text, " \t-;\n"), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
