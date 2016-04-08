from enum import Enum
from core.inputfile import Section
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
        ("compatibility",      "COMPATIBILITY"),
        ("",                   "REPORT_CONTROLS"),
        ("",                   "REPORT_INPUT"),
        ("flow_units",         "FLOW_UNITS"),
        ("infiltration",       "INFILTRATION"),
        ("flow_routing",       "FLOW_ROUTING"),
        ("link_offsets",       "LINK_OFFSETS"),
        ("min_slope",          "MIN_SLOPE"),
        ("allow_ponding",      "ALLOW_PONDING"),
        ("",                   "SKIP_STEADY_STATE"),
        ("ignore_rainfall",    "IGNORE_RAINFALL"),
        ("ignore_rdii",        "IGNORE_RDII"),
        ("ignore_snowmelt",    "IGNORE_SNOWMELT"),
        ("ignore_groundwater", "IGNORE_GROUNDWATER"),
        ("ignore_routing",     "IGNORE_ROUTING"),
        ("ignore_quality",     "IGNORE_QUALITY")))
    """Mapping between attribute name and name used in input file"""

    old_flow_routing = {
        "UF": FlowRouting.STEADY,
        "KW": FlowRouting.KINWAVE,
        "DW": FlowRouting.DYNWAVE}
    """Mapping from old flow routing names to FlowRouting enumeration"""

    section_comments = (";; Dates", ";; Time Steps", ";; Dynamic Wave")

    def __init__(self):
        Section.__init__(self)

        self.dates = Dates()
        self.time_steps = TimeSteps()
        self.dynamic_wave = DynamicWave()

        self.flow_units = FlowUnits.CFS
        """FlowUnits: units in use for flow values"""

        self.infiltration = "HORTON"
        """
        Infiltration computation model of rainfall into the 
        upper soil zone of subcatchments. Use one of the following:
        HORTON, MODIFIED_HORTON, GREEN_AMPT, MODIFIED_GREEN_AMPT, CURVE_NUMBER
        """

        self.flow_routing = FlowRouting.KINWAVE
        """Method used to route flows through the drainage system"""

        self.link_offsets = LinkOffsets.DEPTH
        """
        Convention used to specify the position of a link offset
        above the invert of its connecting node
        """

        self.ignore_rainfall = False
        """True to ignore all rainfall data and runoff calculations"""

        self.ignore_rdii = False
        """True to ignore all rdii calculations"""

        self.ignore_snowmelt = False
        """
        True to ignore snowmelt calculations 
        even if a project contains snow pack objects
        """

        self.ignore_groundwater = False
        """
        True to ignored groundwater calculations 
        even if the project contains aquifer objects
        """

        self.ignore_routing = False
        """True to only compute runoff even if the project contains drainage system links and nodes"""

        self.ignore_quality = False
        """
        True to ignore pollutant washoff, routing, and treatment 
        even in a project that has pollutants defined
        """

        self.allow_ponding = False
        """
        True to allow excess water to collect atop nodes
        and be re-introduced into the system as conditions permit
        """

        self.min_slope = 0.0
        """Minimum value allowed for a conduit slope"""

        self.temp_dir = ""
        """Directory where model writes its temporary files"""

        self.compatibility = 5
        """SWMM Version compatibility"""

    def get_text(self):
        """Contents of this item formatted for writing to file"""
        # First, add the values in this section stored directly in this class
        text_list = [Section.get_text(self)]
        if self.dates is not None:  # Add the values stored in Dates class
            text_list.append(General.section_comments[0])
            text_list.append(self.dates.get_text().replace(self.SECTION_NAME + '\n', ''))
        if self.time_steps is not None:  # Add the values stored in TimeSteps class
            text_list.append(General.section_comments[1])
            text_list.append(self.time_steps.get_text().replace(self.SECTION_NAME + '\n', ''))
        if self.dynamic_wave is not None:  # Add the values stored in DynamicWave class
            text_list.append(General.section_comments[2])
            text_list.append(self.dynamic_wave.get_text().replace(self.SECTION_NAME + '\n', ''))
        return '\n'.join(text_list)

    def set_text(self, new_text):
        """Read this section from the text representation"""

        # Skip the comments we insert automatically
        for comment in General.section_comments:
            new_text = new_text.replace(comment + '\n', '')

        for line in new_text.splitlines():
            line = self.set_comment_check_section(line)
            if line.strip():
                # Set fields from metadata if this section has metadata
                tried_set = False
                for set_here in (self, self.dates, self.time_steps, self.dynamic_wave):
                    (attr_name, attr_value) = set_here.get_attr_name_value(line)
                    if attr_name:
                        try:
                            tried_set = True

                            if attr_name == "flow_routing" and General.old_flow_routing.has_key(attr_value.upper()):
                                # Translate from old flow routing name to new flow routing name
                                attr_value = General.old_flow_routing[attr_value.upper()]

                            set_here.setattr_keep_type(attr_name, attr_value)
                        except Exception as e:
                            print("options.General.text could not set " + attr_name + '\n' + str(e))
                if not tried_set:
                    print("options.General.text skipped: " + line)
