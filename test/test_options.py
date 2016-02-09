from core.epanet import options
from core.epanet.options import hydraulics
from core.epanet.options import map
from core.epanet.options import quality
import unittest


class SimpleOptionsTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_options = options

    def setUp(self):

        self.my_HydraulicsOptions = hydraulics.HydraulicsOptions()
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

        self.my_MapOptions = map.MapOptions()
        self.my_MapOptions.map = ""

        self.my_quality = quality.QualityOptions()
        self.my_quality.quality = quality.QualityAnalysisType.CHEMICAL
        self.my_quality.chemical_name = "DummyChemical"
        self.my_quality.mass_units = "mg/L"
        self.my_quality.diffusivity = 1.0
        self.my_quality.trace_node = ""
        self.my_quality.tolerance = 0.01

    def runTest(self):

        name = self.my_options.hydraulics.HydraulicsOptions.SECTION_NAME
        assert name == "[OPTIONS]"
        assert self.my_HydraulicsOptions.flow_units == hydraulics.FlowUnits.CFS
        assert self.my_HydraulicsOptions.demand_multiplier == 1.1
        assert self.my_MapOptions.map == ""
        assert self.my_quality.chemical_name == "DummyChemical"
        # assert self.my_HydraulicsOptions.text == "[OPTIONS]", 'incorrect options block'
