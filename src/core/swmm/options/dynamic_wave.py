from enum import Enum

from core.project_base import Section
from core.metadata import Metadata


class InertialDamping(Enum):
    """Options for inertial damping"""
    NONE = 1
    PARTIAL = 2
    FULL = 3


class NormalFlowLimited(Enum):
    """Condition to be checked for supercritical flow"""
    SLOPE = 1
    FROUDE = 2
    BOTH = 3


class ForceMainEquation(Enum):
    """Equation to be used for friction losses"""
    H_W = 1
    D_W = 2


class SurchargeMethod(Enum):
    """Mmethod used to handle surcharging"""
    EXTRAN = 1
    SLOT = 2


class DynamicWave(Section):
    """SWMM Dynamic Wave Options"""

    SECTION_NAME = "[OPTIONS]"

    #     attribute,             input_name,            label,               default, english, metric, hint
    metadata = Metadata((
        ("inertial_damping",    "INERTIAL_DAMPING",    "Inertial Damping"),
        ("normal_flow_limited", "NORMAL_FLOW_LIMITED", "Normal Flow Limited"),
        ("force_main_equation", "FORCE_MAIN_EQUATION", "Force Main Equation"),
        ("surcharge_method",    "SURCHARGE_METHOD",    "Surcharge Method"),
        ("variable_step",       "VARIABLE_STEP",       "Variable Step",        "0.0", "sec", "sec"),
        ("lengthening_step",    "LENGTHENING_STEP",    "Lengthening Step",     "0.0", "sec", "sec"),
        ("min_surface_area",    "MIN_SURFAREA",        "Minimum Surface Area", "0.0"),
        ("max_trials",          "MAX_TRIALS",          "Maximum Trials",       "8"),
        ("head_tolerance",      "HEAD_TOLERANCE",      "Head Tolerance",     "0.005", "ft",  "m"),
        ("minimum_step",        "MINIMUM_STEP",        "Minimum Step",         "0.5", "sec", "sec"),
        ("threads",             "THREADS",             "Threads")))
    """Mapping between attribute name and name used in input file"""

    def __init__(self):
        Section.__init__(self)


        ## How the inertial terms in the Saint Venant momentum equation
        ## will be handled under dynamic wave flow routing
        self.inertial_damping = InertialDamping.PARTIAL

        ## Which condition is checked to determine if flow in a conduit
        ## is supercritical and should thus be limited to the normal flow
        self.normal_flow_limited = NormalFlowLimited.BOTH

        ## Establishes whether the Hazen-Williams (H-W) or the Darcy-Weisbach (D-W) equation will be used to
        ## compute friction losses for pressurized flow in conduits that have been assigned a Circular Force
        ## Main cross-section shape. The default is H-W.
        self.force_main_equation = ForceMainEquation.H_W

        ## The EXTRAN method continues to use the traditional Surcharge Algorithm to update the head at surcharged nodes.
        ## The new SLOT option attaches a Preissmann Slot to closed conduits flowing more than 98.5% full that eliminates
        ## the need to switch to the Surcharge Algorithm for surcharged nodes.
        self.surcharge_method = SurchargeMethod.EXTRAN

        ## Time step, in seconds, used to lengthen conduits under
        ## dynamic wave routing, so that they meet the
        ## Courant stability criterion under full-flow conditions
        self.lengthening_step = '0'

        ## Safety factor applied to a variable time step computed for each
        ## time period under dynamic wave flow routing
        self.variable_step = '0.75'

        ## Minimum surface area used at nodes when computing
        ## changes in water depth under dynamic wave routing
        self.min_surface_area = '12.557'

        ## The maximum number of trials allowed during a time step to reach convergence
        ## when updating hydraulic heads at the conveyance system's nodes. The default value is 8.
        self.max_trials = '8'

        ## Difference in computed head at each node between successive trials below
        ## which the flow solution for the current time step is assumed to have converged.
        ## The default tolerance is 0.005 ft (0.0015 m).
        self.head_tolerance = '0.005'

        ## Smallest time step allowed when variable time steps are used for dynamic
        ## wave flow routing. The default value is 0.5 seconds.
        self.minimum_step = '0.5'

        ## Number of parallel computing threads to use for dynamic wave flow routing
        ## on machines equipped with multi-core processors.
        self.threads = ''
