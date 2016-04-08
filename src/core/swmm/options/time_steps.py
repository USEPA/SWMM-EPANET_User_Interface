import core.inputfile
from core.metadata import Metadata


class TimeSteps(core.inputfile.Section):
    """SWMM Time Step Options"""

    SECTION_NAME = "[OPTIONS]"

    #    attribute,                  input_name, label, default, english, metric, hint
    metadata = Metadata((
        ("",                         "COMPATIBILITY"),
        ("",                         "REPORT_CONTROLS"),
        ("",                         "REPORT_INPUT"),
        ("skip_steady_state",        "SKIP_STEADY_STATE"),
        ("report_step",              "REPORT_STEP"),
        ("wet_step",                 "WET_STEP"),
        ("dry_step",                 "DRY_STEP"),
        ("routing_step",             "ROUTING_STEP"),
        ("",                         "INERTIAL_DAMPING"),
        ("",                         "NORMAL_FLOW_LIMITED"),
        ("",                         "FORCE_MAIN_EQUATION"),
        ("",                         "VARIABLE_STEP"),
        ("",                         "LENGTHENING_STEP"),
        ("",                         "MIN_SURFAREA"),
        ("",                         "HEAD_TOLERANCE"),
        ("system_flow_tolerance",    "SYS_FLOW_TOL"),
        ("lateral_inflow_tolerance", "LAT_FLOW_TOL"),
        ("",                         "MINIMUM_STEP"),
        ("",                         "THREADS")))
    """Mapping between attribute name and name used in input file"""

    TIME_FORMAT = "hh:mm:ss"

    def __init__(self):
        core.inputfile.Section.__init__(self)

        self.skip_steady_state = False
        """bool: True to skip flow routing computations during steady state periods
            of a simulation. The last set of computed flows will be used.
        """

        self.report_step = "00:15:00"
        """str: Time interval for reporting of computed results."""

        self.wet_step = "00:05:00"
        """str: Time step length used to compute runoff from subcatchments during
        periods of rainfall or when ponded water remains on the surface.
        """

        self.dry_step = "01:00:00"
        """str: Time step length used for runoff computations
        (consisting essentially of pollutant buildup) 
        during periods when there is no rainfall and no ponded water.
        """

        self.routing_step = "00:05:00"
        """str: Time step used for routing flows and
        water quality constituents through the conveyance system
        """

        self.sys_flow_tol = 5
        """the maximum percent difference between total system inflow and
        total system outflow which can occur in order for the SKIP_STEADY_STATE
        option to take effect. The default is 5 percent.
        """

        self.lat_flow_tol = 5
        """the maximum percent difference between the current and previous
        lateral inflow at all nodes in the conveyance system in order for the
        SKIP_STEADY_STATE option to take effect. The default is 5 percent.
        """