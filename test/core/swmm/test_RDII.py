import unittest
from core.inputfile import Section
from core.swmm.project import Project
from core.swmm.hydraulics.node import RDIInflow


class SimpleRDIITest(unittest.TestCase):
    """Test RDII section"""

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
        assert Section.match_omit(project_section.get_text(), test_text, " \t-;\n")