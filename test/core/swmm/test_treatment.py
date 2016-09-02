import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match
from core.swmm.hydraulics.node import Treatment
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class SimpleTreatmentTest(unittest.TestCase):

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_bod(self):
        """BOD first order decay, from SWMM 5.1 manual"""
        test_text = "Node23 BOD C = BOD * exp(-0.05*HRT) "
        # --Test set_text
        self.my_options = Treatment()
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

    def test_lead(self):
        """Lead removal 20% of TSS removal"""
        test_text = "Node23 Lead R = 0.2 * R_TSS"
        self.my_options = Treatment()
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)


    def test_treatment_section(self):
        """Test TREATMENT section"""
        test_text = r"""
[TREATMENT]
;;                                  Results: R or C
;;                                  R-Fraction removal
;;                                  C-efflument concentration
;;Node             Pollutant        Result = Func
;;----------------------------------------------------------------------
  Node23            BOD              C = BOD * exp(-0.05*HRT)
  Node24            Lead             R = 0.2 * R_TSS
        """
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.treatment
        assert match_omit(project_section.get_text(), test_text, " \t-;\n")

def main():
    unittest.main()

if __name__ == "__main__":
    main()
