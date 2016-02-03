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
    HW = 1
    DW = 2


class DynamicWave(core.inputfile.Section):
    """SWMM Dynamic Wave Options"""

    SECTION_NAME = "[OPTIONS]"

    # @staticmethod
    # def default():
    #     return Options(Options.SECTION_NAME, None, None, -1)

    def __init__(self):
        core.inputfile.Section.__init__(self)
        # TODO: parse "value" argument to extract values for each field, after setting default values below

        self.inertial_damping = InertialDamping.NONE
        """
        How the inertial terms in the Saint Venant momentum equation
        will be handled under dynamic wave flow routing
        """

        self.normal_flow_limited = NormalFlowLimited.SLOPE
        """
        Which condition is checked to determine if flow in a conduit
        is supercritical and should thus be limited to the normal flow
        """

        self.force_main_equation = ForceMainEquation.HW
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