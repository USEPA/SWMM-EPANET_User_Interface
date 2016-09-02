import unittest
from core.swmm.inp_reader_sections import RDIInflowReader
from core.swmm.inp_writer_sections import RDIInflowWriter
from core.swmm.hydraulics.node import RDIInflow
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class SimpleRDIITest(unittest.TestCase):
    """Test RDII section"""
    TEST_TEXTS = ["NODE2  UHGROUP1 12.0 "]
    SOURCE_TEXTS =[r"""
[RDII]
;;Node             UHgroup          SewerArea
;;----------------------------------------------------------------------
  80408            FLOW             80408
  81009            FLOW             81009
  82309            FLOW             82309
        """]

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_one_rdii(self):
        """Test one set of rdii"""
        for test_text in self.TEST_TEXTS:
            my_options = RDIInflowReader.read(test_text)
            actual_text = RDIInflowWriter.as_text(my_options)
            msg = '\nSet:'+test_text+'\nGet:'+actual_text
            self.assertTrue(match(actual_text, test_text), msg)

    def test_rdii_section(self):
        for source_text in self.SOURCE_TEXTS:
            section_from_text = self.project_reader.read_rdii.read(source_text)
            actual_text = self.project_writer.write_rdii.as_text(section_from_text)
            msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
            self.assertTrue(match_omit(actual_text, source_text, " \t-;\n"), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
