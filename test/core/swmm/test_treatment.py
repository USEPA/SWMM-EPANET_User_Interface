import unittest
from core.swmm.inp_reader_sections import TreatmentReader
from core.swmm.inp_writer_sections import TreatmentWriter
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
        my_options = TreatmentReader.read(test_text)
        actual_text = TreatmentWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_lead(self):
        """Lead removal 20% of TSS removal"""
        test_text = "Node23 Lead R = 0.2 * R_TSS"
        my_options = TreatmentReader.read(test_text)
        actual_text = TreatmentWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)


    def test_treatment_section(self):
        """Test TREATMENT section"""
        source_text = r"""
[TREATMENT]
;;                                  Results: R or C
;;                                  R-Fraction removal
;;                                  C-efflument concentration
;;Node             Pollutant        Result = Func
;;----------------------------------------------------------------------
  Node23            BOD              C = BOD * exp(-0.05*HRT)
  Node24            Lead             R = 0.2 * R_TSS
        """
        section_from_text = self.project_reader.read_treatment.read(source_text)
        actual_text = self.project_writer.write_treatment.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match(actual_text, source_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
