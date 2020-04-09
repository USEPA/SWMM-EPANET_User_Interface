from enum import Enum
from core.project_base import Section
from core.metadata import Metadata
from core.swmm.options.dates import Dates
from core.swmm.options.dynamic_wave import DynamicWave
from core.swmm.options.time_steps import TimeSteps


class FlowUnits(Enum):
    """Flow Units"""
    CFS = 1
    GPM = 2
    MGD = 3
    CMS = 4
    LPS = 5
    MLD = 6

flow_units_metric = [FlowUnits.CMS, FlowUnits.LPS, FlowUnits.MLD]


class FlowRouting(Enum):
    """Flow Routing Method"""
    STEADY = 1
    KINWAVE = 2
    DYNWAVE = 3


class LinkOffsets(Enum):
    """Convention for Link Offsets"""
    DEPTH = 1
    ELEVATION = 2


class General(Section):
    """SWMM General Options"""

    SECTION_NAME = "[OPTIONS]"

    #    attribute,            input_name, label, default, english, metric, hint
    metadata = Metadata((
        ("temp_dir",           "TEMPDIR"),
        ("compatibility",      "COMPATIBILITY"),
        ("flow_units",         "FLOW_UNITS"),
        ("infiltration",       "INFILTRATION"),
        ("flow_routing",       "FLOW_ROUTING"),
        ("link_offsets",       "LINK_OFFSETS"),
        ("min_slope",          "MIN_SLOPE"),
        ("allow_ponding",      "ALLOW_PONDING"),
        ("ignore_rainfall",    "IGNORE_RAINFALL"),
        ("ignore_rdii",        "IGNORE_RDII"),
        ("ignore_snowmelt",    "IGNORE_SNOWMELT"),
        ("ignore_groundwater", "IGNORE_GROUNDWATER"),
        ("ignore_routing",     "IGNORE_ROUTING"),
        ("ignore_quality",     "IGNORE_QUALITY")))
    """Mapping between attribute name and name used in input file"""

    section_comments = (";; Dates", ";; Time Steps", ";; Dynamic Wave")

    def __init__(self):
        Section.__init__(self)

        self.dates = Dates()
        self.time_steps = TimeSteps()
        self.dynamic_wave = DynamicWave()

        ## FlowUnits: units in use for flow values
        self.flow_units = FlowUnits.CFS

        ## Infiltration computation model of rainfall into the
        ## upper soil zone of subcatchments. Use one of the following:
        ## HORTON, MODIFIED_HORTON, GREEN_AMPT, MODIFIED_GREEN_AMPT, CURVE_NUMBER
        self.infiltration = "HORTON"

        ## Method used to route flows through the drainage system
        self.flow_routing = FlowRouting.KINWAVE

        ## Convention used to specify the position of a link offset
        ## above the invert of its connecting node
        self.link_offsets = LinkOffsets.DEPTH

        ## True to ignore all rainfall data and runoff calculations
        self.ignore_rainfall = False

        ## True to ignore all rdii calculations
        self.ignore_rdii = False

        ## True to ignore snowmelt calculations
        ## even if a project contains snow pack objects
        self.ignore_snowmelt = False

        ## True to ignored groundwater calculations
        ## even if the project contains aquifer objects
        self.ignore_groundwater = False

        ## True to only compute runoff even if the project contains drainage system links and nodes
        self.ignore_routing = False

        ## True to ignore pollutant washoff, routing, and treatment
        ## even in a project that has pollutants defined
        self.ignore_quality = False

        ## True to allow excess water to collect atop nodes
        ## and be re-introduced into the system as conditions permit
        self.allow_ponding = False

        ## Minimum value allowed for a conduit slope
        self.min_slope = "0.0"

        ## Directory where model writes its temporary files
        self.temp_dir = ""

        ## SWMM Version compatibility
        self.compatibility = "5"

