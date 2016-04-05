from enum import Enum

import core.inputfile


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


class DynamicWave(core.inputfile.Section):
    """SWMM Dynamic Wave Options"""

    SECTION_NAME = "[OPTIONS]"

    field_dict = {
     "INERTIAL_DAMPING": "inertial_damping",
     "NORMAL_FLOW_LIMITED": "normal_flow_limited",
     "FORCE_MAIN_EQUATION": "force_main_equation",
     "VARIABLE_STEP": "variable_step",
     "LENGTHENING_STEP": "lengthening_step",
     "MIN_SURFAREA": "min_surface_area",
     "MAX_TRIALS": "max_trials",
     "HEAD_TOLERANCE": "head_tolerance",
     "SYS_FLOW_TOL": "system_flow_tolerance",
     "LAT_FLOW_TOL": "lateral_inflow_tolerance",
     "MINIMUM_STEP": "minimum_step",
     "THREADS": "threads"}
    """Mapping from label used in file to field name"""

    def __init__(self):
        core.inputfile.Section.__init__(self)

        self.inertial_damping = InertialDamping.NONE
        """
        How the inertial terms in the Saint Venant momentum equation
        will be handled under dynamic wave flow routing
        """

        self.normal_flow_limited = NormalFlowLimited.BOTH
        """
        Which condition is checked to determine if flow in a conduit
        is supercritical and should thus be limited to the normal flow
        """

        self.force_main_equation = ForceMainEquation.H_W
        """
        Establishes whether the Hazen-Williams (H-W) or the Darcy-Weisbach (D-W) equation will be used to
        compute friction losses for pressurized flow in conduits that have been assigned a Circular Force
        Main cross-section shape. The default is H-W.
        """

        self.lengthening_step = 0.0
        """
        Time step, in seconds, used to lengthen conduits under 
        dynamic wave routing, so that they meet the 
        Courant stability criterion under full-flow conditions
        """

        self.variable_step = 0.0
        """
        Safety factor applied to a variable time step computed for each
        time period under dynamic wave flow routing
        """

        self.min_surface_area = 0.0
        """
        Minimum surface area used at nodes when computing 
        changes in water depth under dynamic wave routing
        """

        self.max_trials = 8
        """
        The maximum number of trials allowed during a time step to reach convergence
        when updating hydraulic heads at the conveyance system’s nodes. The default value is 8.
        """

        self.head_tolerance = 0.005
        """
        Difference in computed head at each node between successive trials below
        which the flow solution for the current time step is assumed to have converged.
        The default tolerance is 0.005 ft (0.0015 m).
        """

        self.minimum_step = 0.5
        """
        Smallest time step allowed when variable time steps are used for dynamic
        wave flow routing. The default value is 0.5 seconds.
        """

        self.threads = 1
        """
        Number of parallel computing threads to use for dynamic wave flow routing
        on machines equipped with multi-core processors. The default is 1.
        """