import unittest
from core.epanet.options.options import Options
from core.epanet.options import hydraulics
from core.epanet.options import map
from core.epanet.options import quality
from core.epanet.inp_reader_sections import OptionsReader
from core.epanet.inp_writer_sections import OptionsWriter
from test.core.section_match import match


class SimpleOptionsTest(unittest.TestCase):
    """Test Options section"""

    def test_get(self):
        """Test get_text using matches"""
        # Create options instance
        my_options = Options()


        # Set data attributes
        my_options.hydraulics.flow_units = hydraulics.FlowUnits.CFS
        my_options.hydraulics.head_loss = hydraulics.HeadLoss.H_W
        my_options.hydraulics.specific_gravity = 1.0
        my_options.hydraulics.relative_viscosity = 1.0
        my_options.hydraulics.maximum_trials = 40
        my_options.hydraulics.accuracy = 0.001
        my_options.hydraulics.unbalanced = hydraulics.Unbalanced.STOP
        my_options.hydraulics.unbalanced_continue = 10
        my_options.hydraulics.default_pattern = "1"
        my_options.hydraulics.demand_multiplier = 1.1
        my_options.hydraulics.emitter_exponent = 0.5
        my_options.hydraulics.check_frequency = 2
        my_options.hydraulics.max_check = 10
        my_options.hydraulics.damp_limit = 0.0

        # Set data attributes
        my_options.map = ""

        # Set data attributes
        my_options.quality.quality = quality.QualityAnalysisType.CHEMICAL
        my_options.quality.chemical_name = "DummyChemical"
        my_options.quality.mass_units = "mg/L"
        my_options.quality.diffusivity = 1.0
        my_options.quality.trace_node = ""
        my_options.quality.tolerance = 0.01

        # Assert section name
        name = my_options.hydraulics.SECTION_NAME
        assert name == "[OPTIONS]"

        # These seem to be redundant with set up--- xw commented
        # assert self.my_HydraulicsOptions.flow_units == hydraulics.FlowUnits.CFS
        # assert self.my_HydraulicsOptions.demand_multiplier == 1.1
        # assert self.my_quality.chemical_name == "DummyChemical"
        # assert self.my_HydraulicsOptions.get_text() == "[OPTIONS]", 'incorrect options block'

        # Use matches method to test hydraulic and quality options
        expected_text = " [OPTIONS]\n" \
                        " Unbalanced         	STOP\n"\
                        " MAXCHECK           	10\n"\
                        " Emitter Exponent   	0.5\n"\
                        " Trials             	40\n"\
                        " DAMPLIMIT          	0.0\n"\
                        " Viscosity          	1.0\n"\
                        " Demand Multiplier  	1.1\n"\
                        " CHECKFREQ          	2\n"\
                        " Specific Gravity   	1.0\n"\
                        " Pattern            	1\n"\
                        " Units              	CFS\n"\
                        " Accuracy           	0.001\n"\
                        " Headloss           	H-W\n" \
                        " Quality            	DummyChemical mg/L\n" \
                        " Diffusivity         	1.0\n" \
                        " Tolerance           	0.01"

        actual_text = OptionsWriter.as_text(my_options)
        msg = '\nSet:\n' + expected_text + '\nGet:\n' + actual_text
        self.assertTrue(match(actual_text, expected_text), msg)

    def test_setget(self):
        """Test both set_text and get_text of Options, data from Net1.inp"""

        test_text = """
        [OPTIONS]
         Units              	GPM
         Headloss           	H-W
         Specific Gravity   	1.0
         Viscosity          	1.0
         Trials             	40
         Accuracy           	0.001
         CHECKFREQ          	2
         MAXCHECK           	10
         DAMPLIMIT          	0
         Unbalanced         	Continue 10
         Pattern            	1
         Demand Multiplier  	1.0
         Emitter Exponent   	0.5
         Quality            	Chlorine mg/L
         Diffusivity        	1.0
         Tolerance          	0.01
         """

        my_options = OptionsReader.read(test_text)
        actual_text = OptionsWriter.as_text(my_options)
        msg = '\nSet:\n' + test_text + '\nGet:\n' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()