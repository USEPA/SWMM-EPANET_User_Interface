import unittest
from core.swmm.inp_reader_sections import RainGageReader
from core.swmm.inp_writer_sections import RainGageWriter
from core.swmm.hydrology.raingage import RainGage
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class SimpleRainGageTest(unittest.TestCase):
    """Test RAINGAGES section"""

    TEST_TEXTS = ["RainGage         INTENSITY 0:05   1.0    TIMESERIES 2-yr "]
    SOURCE_TEXTS =["""[RAINGAGES]
;;               Rain      Time   Snow   Data
;;Name           Type      Intrvl Catch  Source
;;-------------- --------- ------ ------ ----------
RainGage         INTENSITY 0:05   1.0    TIMESERIES 2-yr"""]

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_one_raingage(self):
        """Test one rain gage"""
        for test_text in self.TEST_TEXTS:
            my_options = RainGageReader.read(test_text)
            actual_text = RainGageWriter.as_text(my_options)
            msg = '\nSet:'+test_text+'\nGet:'+actual_text
            self.assertTrue(match(actual_text, test_text), msg)

    def test_raingage_section(self):
        """Test RAINGAGES section"""
        for source_text in self.SOURCE_TEXTS:
            section_from_text = self.project_reader.read_raingages.read(source_text)
            actual_text = self.project_writer.write_raingages.as_text(section_from_text)
            msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
            self.assertTrue(match_omit(actual_text, source_text, " \t-;\n"), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
