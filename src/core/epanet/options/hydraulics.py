from enum import Enum
from core.inputfile import Section


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

    field_dict = {
        "Units": "flow_units",
        "Headloss": "head_loss",
        "Specific Gravity": "specific_gravity",
        "Viscosity": "viscosity",
        "Trials": "maximum_trials",
        "Accuracy": "accuracy",
        "CHECKFREQ": "check_frequency",
        "MAXCHECK": "max_check",
        "DAMPLIMIT": "damp_limit",
        "Unbalanced": "unbalanced_continue",
        "Pattern": "default_pattern",
        "Demand Multiplier": "demand_multiplier",
        "Emitter Exponent": "emitter_exponent",
        "Quality": "",
        "Diffusivity": "",
        "Tolerance": ""}
    """Mapping from label used in file to field name"""

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

    @property
    def text(self):
        text_list = []
        for label, attr_name in HydraulicsOptions.field_dict.items():
            attr_value = ""
            if label == "Unbalanced":
                if self.unbalanced == Unbalanced.STOP:
                    attr_value = "STOP"
                else:
                    attr_value = "Continue " + str(self.unbalanced_continue)

            elif label and attr_name and hasattr(self, attr_name):
                attr_value = str(getattr(self, attr_name))

            if attr_value:
                text_list.append(self.field_format.format(label, attr_value))

        return '\n'.join(text_list)

    @text.setter
    def text(self, new_text):
        for line in new_text.splitlines():
            try:
                if not line.startswith((';', '[')):
                    lower_line = line.lower().strip()
                    for dict_tuple in self.field_dict.items():
                        key = dict_tuple[0]
                        if lower_line.startswith(key.lower()) and lower_line[len(key)] in (' ', '\t'):
                            attr_name = dict_tuple[1]
                            if attr_name == "unbalanced_continue":
                                fields = line.split()
                                self.unbalanced = Unbalanced[fields[1].upper()]
                                if len(fields) > 2:
                                    self.unbalanced_continue = fields[2]
                            else:
                                attr_value = line[len(key) + 1:].strip()
                                setattr(self, attr_name, attr_value)
            except:
                print("HydraulicsOptions skipping input line: " + line)
