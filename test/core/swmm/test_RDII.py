import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match
from core.swmm.hydraulics.node import RDIInflow
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class SimpleRDIITest(unittest.TestCase):
    """Test RDII section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_one_rdii(self):
        """Test one set of rdii"""
        self.my_options = RDIInflow()
        test_text = "NODE2  UHGROUP1 12.0 "
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

    def test_rdii_section(self):
        test_text = r"""
[RDII]
;;Node             UHgroup          SewerArea
;;----------------------------------------------------------------------
  80408            FLOW             80408
  81009            FLOW             81009
  82309            FLOW             82309
        """
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.rdii
        assert match_omit(project_section.get_text(), test_text, " \t-;\n")

def main():
    unittest.main()

if __name__ == "__main__":
    main()
