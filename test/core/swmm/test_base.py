import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit, match_omit_nocase


class BastForTests(unittest.TestCase):
    """Test LIDUSAGE section"""

    def __init__(self):
        """"""
        unittest.TestCase.__init__(self)
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def set_base(self, reader, writer, sreader, swriter, rows, sections):
        self.row_reader = reader
        self.row_writer = writer
        self.section_reader = sreader
        self.section_writer = swriter
        self.TEST_TEXTS = rows
        self.SECTION_TEXTS = sections

    def test_a_row(self):
        """Test aquifer parameters from SWMM 5.1 manual"""
        for test_text in self.TEST_TEXTS:
            my_options = self.row_reader.read(test_text)
            actual_text = self.row_writer.as_text(my_options)
            msg = '\nSet:' + test_text + '\nGet:' + actual_text
            self.assertTrue(match(actual_text, test_text), msg)

    def test_section(self):
        """Test LIDUSAGE section through Project class
         Test failed as current LID usage only contains one line of LID usage
         Also code compained when I have special character in the comment lines"""

        for section_text in self.SECTION_TEXTS:
            section_from_text = self.section_reader.read(section_text)
            actual_text = self.section_writer.as_text(section_from_text)
            msg = '\nSet:' + section_text + '\nGet:' + actual_text
            self.assertTrue(match_omit(actual_text, section_text, " \t-;\n"), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()