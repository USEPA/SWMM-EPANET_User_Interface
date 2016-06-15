import unittest
from core.epanet.options.options import Options
from core.epanet.options import quality


class SimpleQualityTest(unittest.TestCase):
    """Test Quality section"""

    def test_get(self):
        """Test get_text of quality sections"""
        self.my_options = Options()
        self.my_quality = quality.QualityOptions()
        self.my_quality.quality = quality.QualityAnalysisType.CHEMICAL
        self.my_quality.chemical_name = "DummyChemical"
        self.my_quality.mass_units = "mg/L"
        self.my_quality.diffusivity = 1.0
        self.my_quality.trace_node = ""
        self.my_quality.tolerance = 0.01
        name = self.my_options.quality.SECTION_NAME
        assert name == "[OPTIONS]"
        assert self.my_quality.chemical_name == "DummyChemical"
        # assert self.my_HydraulicsOptions.get_text() == "[OPTIONS]", 'incorrect options block'
        expected_text = " Quality            	DummyChemical mg/L\n" + \
                        " Diffusivity         	1.0\n" + \
                        " Tolerance           	0.01\n"

        actual_text = self.my_quality.get_text()
        assert actual_text == expected_text

        self.my_quality.quality = quality.QualityAnalysisType.TRACE
        self.my_quality.diffusivity = 2.0
        self.my_quality.trace_node = "XX"
        self.my_quality.tolerance = 0.02
        self.my_quality.mass_units = ""

        expected_text = " Quality            	Trace XX\n" + \
                        " Diffusivity         	2.0\n" + \
                        " Tolerance           	0.02\n"

        actual_text = self.my_quality.get_text()
        assert actual_text == expected_text

    def test_setget(self):
         test_text = " Quality            	DummyChemical mg/L\n" \
                     " Diffusivity         	1.0\n" \
                     " Tolerance           	0.01\n"
         # self.my_options = Options()
         self.my_quality = quality.QualityOptions()
         self.my_quality.set_text(test_text)
         actual_text = self.my_quality.get_text()
         assert self.my_quality.matches(test_text)