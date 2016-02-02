from core.inputfile import Section
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
        self.my_options = options
        self.my_options.hydraulics.HydraulicsOptions.flow_units = hydraulics.FlowUnits.CFS
        self.my_options.hydraulics.HydraulicsOptions.head_loss = hydraulics.HeadLoss.H_W
        self.my_options.hydraulics.HydraulicsOptions.specific_gravity = 1.0
        self.my_options.hydraulics.HydraulicsOptions.relative_viscosity = 1.0
        self.my_options.hydraulics.HydraulicsOptions.maximum_trials = 40
        self.my_options.hydraulics.HydraulicsOptions.accuracy = 0.001
        self.my_options.hydraulics.HydraulicsOptions.unbalanced = hydraulics.Unbalanced.STOP
        self.my_options.hydraulics.HydraulicsOptions.unbalanced_continue = 10
        self.my_options.hydraulics.HydraulicsOptions.default_pattern = "1"
        self.my_options.hydraulics.HydraulicsOptions.demand_multiplier = 1.1
        self.my_options.hydraulics.HydraulicsOptions.emitter_exponent = 0.5
        self.my_options.hydraulics.HydraulicsOptions.check_frequency = 2
        self.my_options.hydraulics.HydraulicsOptions.max_check = 10
        self.my_options.hydraulics.HydraulicsOptions.damp_limit = 0.0

        self.my_options.map.MapOptions.map = ""

        self.my_options.quality.quality = quality.Quality.CHEMICAL
        self.my_options.quality.chemical_name = "DummyChemical"
        self.my_options.quality.mass_units = "mg/L"
        self.my_options.quality.relative_diffusivity = 1.0
        self.my_options.quality.trace_node = ""
        self.my_options.quality.tolerance = 0.01

    def runTest(self):

        name = self.my_options.hydraulics.HydraulicsOptions.SECTION_NAME
        assert name == "[OPTIONS]"
        assert self.my_options.hydraulics.HydraulicsOptions.flow_units == hydraulics.FlowUnits.CFS
        assert self.my_options.hydraulics.HydraulicsOptions.demand_multiplier == 1.1
        assert self.my_options.map.MapOptions.map == ""
        assert self.my_options.quality.chemical_name == "DummyChemical"
        # assert self.my_options.to_inp() == "[OPTIONS]", 'incorrect options block'




