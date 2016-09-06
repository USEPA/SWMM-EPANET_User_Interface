import unittest
from core.epanet.inp_reader_sections import QualityOptionsReader
from core.epanet.inp_writer_sections import QualityOptionsWriter
from core.epanet.options import quality
from test.core.section_match import match


class SimpleQualityTest(unittest.TestCase):
    """Test Quality section"""

    def test_get(self):
        """Test get_text of quality sections"""
        my_quality = quality.QualityOptions()
        my_quality.quality = quality.QualityAnalysisType.CHEMICAL
        my_quality.chemical_name = "DummyChemical"
        my_quality.mass_units = "mg/L"
        my_quality.diffusivity = 1.0
        my_quality.trace_node = ""
        my_quality.tolerance = 0.01
        name = my_quality.SECTION_NAME
        assert name == "[OPTIONS]"
        # assert self.my_HydraulicsOptions.get_text() == "[OPTIONS]", 'incorrect options block'
        expected_text = " Quality            	DummyChemical mg/L\n" + \
                        " Diffusivity         	1.0\n" + \
                        " Tolerance           	0.01\n"
        actual_text = QualityOptionsWriter.as_text(my_quality)
        msg = '\nSet:'+expected_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, expected_text), msg)

        my_quality.quality = quality.QualityAnalysisType.TRACE
        my_quality.diffusivity = 2.0
        my_quality.trace_node = "XX"
        my_quality.tolerance = 0.02
        my_quality.mass_units = ""

        expected_text = " Quality            	Trace XX\n" + \
                        " Diffusivity         	2.0\n" + \
                        " Tolerance           	0.02\n"

        actual_text = QualityOptionsWriter.as_text(my_quality)
        msg = '\nSet:'+expected_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, expected_text), msg)

    def test_setget(self):
         test_text = " Quality            	DummyChemical mg/L\n" \
                     " Diffusivity         	1.0\n" \
                     " Tolerance           	0.01\n"
         my_quality = QualityOptionsReader.read(test_text)
         actual_text = QualityOptionsWriter.as_text(my_quality)
         msg = '\nSet:' + test_text + '\nGet:' + actual_text
         self.assertTrue(match(actual_text, test_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
