from core.project_base import Section
from core.metadata import Metadata


class TimeSteps(Section):
    """SWMM Time Step Options"""

    SECTION_NAME = "[OPTIONS]"

    #    attribute,                  input_name, label, default, english, metric, hint
    metadata = Metadata((
        ("skip_steady_state",        "SKIP_STEADY_STATE"),
        ("report_step",              "REPORT_STEP"),
        ("wet_step",                 "WET_STEP"),
        ("dry_step",                 "DRY_STEP"),
        ("routing_step",             "ROUTING_STEP"),
        ("rule_step",                "RULE_STEP"),
        ("system_flow_tolerance",    "SYS_FLOW_TOL", '', '5', '%', '%'),
        ("lateral_inflow_tolerance", "LAT_FLOW_TOL", '', '5', '%', '%')))
    """Mapping between attribute name and name used in input file"""

    TIME_FORMAT = "hh:mm:ss"

    def __init__(self):
        Section.__init__(self)

        self.skip_steady_state = False
        ## bool: True to skip flow routing computations during steady state periods
        ## of a simulation. The last set of computed flows will be used.

        self.report_step = "00:15:00"
        ## str: Time interval for reporting of computed results.

        self.wet_step = "00:05:00"
        ## str: Time step length used to compute runoff from subcatchments during
        ## periods of rainfall or when ponded water remains on the surface.

        self.dry_step = "01:00:00"
        ## str: Time step length used for runoff computations
        ## (consisting essentially of pollutant buildup)
        ## during periods when there is no rainfall and no ponded water.

        self.routing_step = "00:05:00"
        ## str: Time step used for routing flows and
        ## water quality constituents through the conveyance system

        self.rule_step = "00:00:00"
        ## periodic time step for control rule evaluation

        self.system_flow_tolerance = "5"
        ## the maximum percent difference between total system inflow and
        ## total system outflow which can occur in order for the SKIP_STEADY_STATE
        ## option to take effect. The default is 5 percent.

        self.lateral_inflow_tolerance = "5"
        ## the maximum percent difference between the current and previous
        ## lateral inflow at all nodes in the conveyance system in order for the
        ## SKIP_STEADY_STATE option to take effect. The default is 5 percent.