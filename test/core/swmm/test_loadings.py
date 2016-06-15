import unittest
from core.inputfile import Section
from core.swmm.project import Project
from core.swmm.hydrology.subcatchment import InitialLoading


class SimpleLoadingTest(unittest.TestCase):
    """Test LOADINGS section"""

    def test_one_loading(self):
        """Test all options of one Loading"""
        test_text = "SB1   TSS         0.1      Lead         0.01 "
        self.my_options = InitialLoading()
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text() # display purpose
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(self.my_options.matches(test_text), msg)

    def test_loading_section(self):
        """Test LOADINGS section"""
        test_text = r"""
[LOADINGS]
;;Subcatchment     Pollutant   Loading  Pollutant   Loading
;;----------------------------------------------------------
SB1                TSS         0.1      Lead         0.01
        """
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.loadings
        actual_text = project_section.get_text()
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(project_section.matches(test_text), msg)
        # assert Section.match_omit(project_section.get_text(), test_text, " \t-;\n")