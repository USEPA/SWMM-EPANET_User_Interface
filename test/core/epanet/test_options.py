import unittest
from core.epanet.options.options import Options
from core.epanet.options import hydraulics
from core.epanet.options import map
from core.epanet.options import quality


class SimpleOptionsTest(unittest.TestCase):
    """Test Options section"""

    def test_get(self):
        """Test get_text using matches"""

        # Create an instance of Options
        self.my_options = Options()

        # Create hydraulic options instance
        self.my_HydraulicsOptions = hydraulics.HydraulicsOptions()

        # Set data attributes
        self.my_HydraulicsOptions.flow_units = hydraulics.FlowUnits.CFS
        self.my_HydraulicsOptions.head_loss = hydraulics.HeadLoss.H_W
        self.my_HydraulicsOptions.specific_gravity = 1.0
        self.my_HydraulicsOptions.relative_viscosity = 1.0
        self.my_HydraulicsOptions.maximum_trials = 40
        self.my_HydraulicsOptions.accuracy = 0.001
        self.my_HydraulicsOptions.unbalanced = hydraulics.Unbalanced.STOP
        self.my_HydraulicsOptions.unbalanced_continue = 10
        self.my_HydraulicsOptions.default_pattern = "1"
        self.my_HydraulicsOptions.demand_multiplier = 1.1
        self.my_HydraulicsOptions.emitter_exponent = 0.5
        self.my_HydraulicsOptions.check_frequency = 2
        self.my_HydraulicsOptions.max_check = 10
        self.my_HydraulicsOptions.damp_limit = 0.0

        # Create map options instance
        self.my_MapOptions = map.MapOptions()

        # Set data attributes
        self.my_MapOptions.map = ""

        # Create quality options instance
        self.my_quality = quality.QualityOptions()

        # Set data attributes
        self.my_quality.quality = quality.QualityAnalysisType.CHEMICAL
        self.my_quality.chemical_name = "DummyChemical"
        self.my_quality.mass_units = "mg/L"
        self.my_quality.diffusivity = 1.0
        self.my_quality.trace_node = ""
        self.my_quality.tolerance = 0.01

        # Assert section name
        name = self.my_options.hydraulics.SECTION_NAME
        assert name == "[OPTIONS]"

        # These seem to be redundant with set up--- xw commented
        # assert self.my_HydraulicsOptions.flow_units == hydraulics.FlowUnits.CFS
        # assert self.my_HydraulicsOptions.demand_multiplier == 1.1
        # assert self.my_quality.chemical_name == "DummyChemical"
        # assert self.my_HydraulicsOptions.get_text() == "[OPTIONS]", 'incorrect options block'

        # Use matches method to test hydraulic and quality options
        expected_text = " Unbalanced         	STOP\n"\
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
                        " Headloss           	H-W"

        assert self.my_HydraulicsOptions.matches(expected_text)

        # Use matches method to test map options
        assert self.my_MapOptions.map == ""
        expected_text = ""
        assert self.my_MapOptions.matches(expected_text)

    def test_setget(self):
        """Test both set_text and get_text of Options, data from Net1.inp"""

        self.my_options = Options()
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
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()
        assert self.my_options.matches(test_text)