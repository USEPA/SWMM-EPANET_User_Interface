from core.epanet.options.options import Options
from core.epanet.options import hydraulics
from core.epanet.options import map
from core.epanet.options import quality
import unittest


class SimpleQualityTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_options = Options()

    def setUp(self):

        self.my_quality = quality.QualityOptions()
        self.my_quality.quality = quality.QualityAnalysisType.CHEMICAL
        self.my_quality.chemical_name = "DummyChemical"
        self.my_quality.mass_units = "mg/L"
        self.my_quality.diffusivity = 1.0
        self.my_quality.trace_node = ""
        self.my_quality.tolerance = 0.01

    def runTest(self):

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