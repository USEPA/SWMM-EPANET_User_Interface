from enum import Enum
from core.inputfile import Section
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

        self.flow_units = FlowUnits.GPM
        """FlowUnits: units in use for flow values"""

        self.head_loss = HeadLoss.H_W
        """HeadLoss: formula to use for computing head loss"""

        self.specific_gravity = 1.0
        """Ratio of the density of the fluid being modeled to that of water at 4 deg. C"""

        self.viscosity = 1.0
        """Kinematic viscosity of the fluid being modeled relative to that of water at 20 deg. C"""

        self.maximum_trials = 40
        """Maximum number of trials used to solve network hydraulics at each hydraulic time step of a simulation"""

        self.accuracy = 0.001
        """Prescribes the convergence criterion that determines when a hydraulic solution has been reached"""

        self.unbalanced = Unbalanced.STOP
        """Determines what happens if a hydraulic solution cannot be reached within the prescribed number of TRIALS"""

        self.unbalanced_continue = 10
        """If continuing after n trials, continue this many more trials with links held fixed"""

        self.default_pattern = "1"
        """Default demand pattern to be applied to all junctions where no demand pattern was specified"""

        self.demand_multiplier = 1.0
        """Used to adjust the values of baseline demands for all junctions and all demand categories"""

        self.emitter_exponent = 0.5
        """Specifies the power to which the pressure is raised when computing the flow issuing from an emitter"""

        self.check_frequency = 2
        """Undocumented"""

        self.max_check = 10
        """Undocumented"""

        self.damp_limit = 0.0
        """Undocumented"""

        self.hydraulics = Hydraulics.SAVE
        """Either SAVE the current hydraulics solution to a file or USE a previously saved hydraulics solution"""
        """By default do not write this line"""

        self.hydraulics_file = ""
        """Hydraulics file to either use or save"""
        """By default do not write this line"""

    def get_text(self):
        text_list = []
        for meta_item in HydraulicsOptions.metadata:
            attr_value = ""
            if meta_item.input_name == "Unbalanced":
                if self.unbalanced == Unbalanced.STOP:
                    attr_value = "STOP"
                else:
                    attr_value = "Continue " + str(self.unbalanced_continue)
            if attr_value:
                text_list.append(self.field_format.format(meta_item.input_name, attr_value))
            else:
                attr_line = self._get_attr_line(meta_item.input_name, meta_item.attribute)
                if attr_line:
                    text_list.append(attr_line)
        return '\n'.join(text_list)

    def set_text(self, new_text):
        for line in new_text.splitlines():
            try:
                line = line.strip()
                if not line.startswith((';', '[')):
                    lower_line = line.lower()
                    if lower_line:
                        for meta_item in self.metadata:
                            key = meta_item.input_name.lower()
                            if len(lower_line) > len(key):
                                if lower_line.startswith(key) and lower_line[len(key)] in (' ', '\t'):
                                    if meta_item.attribute == "unbalanced_continue":
                                        fields = line.split()
                                        self.unbalanced = Unbalanced[fields[1].upper()]
                                        if len(fields) > 2:
                                            self.unbalanced_continue = fields[2]
                                    else:
                                        attr_value = line[len(key) + 1:].strip()
                                        self.setattr_keep_type(meta_item.attribute, attr_value)
            except:
                print("HydraulicsOptions skipping input line: " + line)
