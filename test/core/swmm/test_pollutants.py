import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from core.swmm.quality import Pollutant
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit, match_keyword_lines

class SimplePollutantTest(unittest.TestCase):
    """Test POLLUTANTS section"""

    TEST_TEXTS = [" Lead             UG/L   0.0        0.0        0          0.0        NO    TSS 0.2 0.0 0.0  "]
    SOURCE_TEXTS = [r"""
[POLLUTANTS]
;;                 Mass   Rain       GW         I&I        Decay      Snow
;;Name             Units  Conc.      Conc.      Conc.      Coeff.     Only  Co-Pollutant
;;------------------------------------------------------------------------------------------
  TSS              MG/L   0.0        0.0        0          0.0        NO    *
  Lead             UG/L   0.0        0.0        0          0.0        NO    TSS 0.2"""]

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_one_pollutant(self):
        """Test one pollutant"""
        for test_text in self.TEST_TEXTS:
            my_options = PollutantReader.read(test_text)
            actual_text = PollutantWriter.as_text(my_options)
            msg = '\nSet:'+test_text+'\nGet:'+actual_text
            self.assertTrue(match(actual_text, test_text), msg)

    def test_pollutant_section(self):
        """Test POLLUTANTS section through Project"""
        for source_text in self.SOURCE_TEXTS:
            section_from_text = self.project_reader.read_pollutants.read(source_text)
            actual_text = self.project_writer.write_pollutants.as_text(section_from_text)
            msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
            self.assertTrue(match_keyword_lines(source_text, actual_text,
                                                keywords_=None, skipped_keywords=None, ignore_trailing_0=True), msg)


def main():
    unittest.main()

if __name__ == "__main__":
    main()
