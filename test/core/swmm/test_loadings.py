import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match
from core.swmm.hydrology.subcatchment import InitialLoading


class SimpleLoadingTest(unittest.TestCase):
    """Test LOADINGS section"""

    def test_one_loading(self):
        """Test all options of one Loading"""
        test_text = "SB1   TSS         0.1"
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
        self.assertTrue(len(project_section.value) == 2, "Expected 2 loadings, found " + str(len(project_section.value)))
        tss = project_section.value[0]
        self.assertTrue(tss.pollutant_name == "TSS", "Expected pollutant name TSS, found " + tss.pollutant_name)
        self.assertTrue(str(tss.initial_buildup) == "0.1", "Expected TSS buildup = 0.1, found " + str(tss.initial_buildup))

        Lead = project_section.value[1]
        self.assertTrue(Lead.pollutant_name == "Lead", "Expected pollutant name Lead, found " + Lead.pollutant_name)
        self.assertTrue(str(Lead.initial_buildup) == "0.01", "Expected Lead buildup = 0.01, found " + str(Lead.initial_buildup))
