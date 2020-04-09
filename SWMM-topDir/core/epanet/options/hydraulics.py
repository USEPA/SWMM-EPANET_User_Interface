from enum import Enum
from core.project_base import Section
from core.metadata import Metadata


class FlowUnits(Enum):
    """Flow Units"""
    CFS = 1
    GPM = 2
    MGD = 3
    IMGD = 4
    AFD = 5
    LPS = 6
    LPM = 7
    MLD = 8
    CMH = 9
    CMD = 10

flow_units_metric = [FlowUnits.LPS, FlowUnits.LPM, FlowUnits.MLD, FlowUnits.CMH, FlowUnits.CMD]


class HeadLoss(Enum):
    """Head Loss"""
    H_W = 1
    D_W = 2
    C_M = 3


class Hydraulics(Enum):
    """Hydraulics"""
    USE = 1
    SAVE = 2


class Unbalanced(Enum):
    """What to do if hydraulic solution cannot be reached"""
    STOP = 1
    CONTINUE = 2


class HydraulicsOptions(Section):
    """EPANET Hydraulics Options"""

    SECTION_NAME = "[OPTIONS]"

    #    attribute,             input_name, label, default, english, metric, hint
    metadata = Metadata((
        ("flow_units",          "Units"),
        ("head_loss",           "Headloss"),
        ("specific_gravity",    "Specific Gravity"),
        ("viscosity",           "Viscosity"),
        ("maximum_trials",      "Trials"),
        ("accuracy",            "Accuracy"),
        ("check_frequency",     "CHECKFREQ"),
        ("max_check",           "MAXCHECK"),
        ("damp_limit",          "DAMPLIMIT"),
        ("unbalanced_continue", "Unbalanced"),
        ("default_pattern",     "Pattern"),
        ("demand_multiplier",   "Demand Multiplier"),
        ("emitter_exponent",    "Emitter Exponent"),
        ("",                    "Quality"),
        ("",                    "Diffusivity"),
        ("",                    "Tolerance")))
    """Mapping between attribute name and name used in input file"""

    def __init__(self):
        Section.__init__(self)

        ## FlowUnits: units in use for flow values
        self.flow_units = FlowUnits.CFS

        ## HeadLoss: formula to use for computing head loss
        self.head_loss = HeadLoss.H_W

        ## Ratio of the density of the fluid being modeled to that of water at 4 deg. C
        self.specific_gravity = 1.0

        ## Kinematic viscosity of the fluid being modeled relative to that of water at 20 deg. C
        self.viscosity = 1.0

        ## Maximum number of trials used to solve network hydraulics at each hydraulic time step of a simulation
        self.maximum_trials = 40

        ## Prescribes the convergence criterion that determines when a hydraulic solution has been reached
        self.accuracy = 0.001

        ## Determines what happens if a hydraulic solution cannot be reached within the prescribed number of TRIALS
        self.unbalanced = Unbalanced.STOP

        ## If continuing after n trials, continue this many more trials with links held fixed
        self.unbalanced_continue = ''

        ## Default demand pattern to be applied to all junctions where no demand pattern was specified
        self.default_pattern = "1"

        ## Default demand pattern object
        self.default_pattern_object = None

        ## Used to adjust the values of baseline demands for all junctions and all demand categories
        self.demand_multiplier = 1.0

        ## Specifies the power to which the pressure is raised when computing the flow issuing from an emitter
        self.emitter_exponent = 0.5

        ## Undocumented
        self.check_frequency = 2

        ## Undocumented
        self.max_check = 10

        ## Undocumented
        self.damp_limit = 0.0

        ## Either SAVE the current hydraulics solution to a file or USE a previously saved hydraulics solution;
        ## By default do not write this line
        self.hydraulics = Hydraulics.SAVE

        ## Hydraulics file to either use or save;
        ## By default do not write this line
        self.hydraulics_file = ""


