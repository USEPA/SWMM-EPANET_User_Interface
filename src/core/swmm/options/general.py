from enum import Enum
from core.inputfile import Section
from core.swmm.options.dates import Dates
from core.swmm.options.dynamicwave import DynamicWave
from core.swmm.options.timesteps import TimeSteps
import core.swmm.hydrology.subcatchment


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

    field_dict = {
     "COMPATIBILITY": "",
     "REPORT_CONTROLS": "",
     "REPORT_INPUT": "",

     "FLOW_UNITS": "flow_units",
     "INFILTRATION": "infiltration",
     "FLOW_ROUTING": "flow_routing",
     "LINK_OFFSETS": "link_offsets",
     "MIN_SLOPE": "min_slope",
     "ALLOW_PONDING": "allow_ponding",
     "SKIP_STEADY_STATE": "",

     "IGNORE_RAINFALL": "ignore_rainfall",
     "IGNORE_RDII": "ignore_rdii",
     "IGNORE_SNOWMELT": "ignore_snowmelt",
     "IGNORE_GROUNDWATER": "ignore_groundwater",
     "IGNORE_ROUTING": "ignore_routing",
     "IGNORE_QUALITY": "ignore_quality",

     "INERTIAL_DAMPING": "",
     "NORMAL_FLOW_LIMITED": "",
     "FORCE_MAIN_EQUATION": "",
     "VARIABLE_STEP": "",
     "LENGTHENING_STEP": "",
     "MIN_SURFAREA": "",
     "MAX_TRIALS": "",
     "HEAD_TOLERANCE": "",
     "SYS_FLOW_TOL": "",
     "LAT_FLOW_TOL": "",
     "MINIMUM_STEP": "",
     "THREADS": ""}
    """Mapping from label used in file to field name"""

    def __init__(self):
        Section.__init__(self)

        self.dates = Dates()
        self.time_steps = TimeSteps()
        self.dynamic_wave = DynamicWave()

        self.flow_units = FlowUnits.CFS
        """FlowUnits: units in use for flow values"""

        self.infiltration = core.swmm.hydrology.subcatchment.HortonInfiltration()
        """
        Infiltration computation model of rainfall into the 
        upper soil zone of subcatchments. Use one of the following:
        HortonInfiltration, GreenAmptInfiltration, or CurveNumberInfiltration
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
        """Minimum value allowed for a conduits slope"""

        self.temp_dir = ""
        """Directory where model writes its temporary files"""

    def get_text(self):
        """Contents of this item formatted for writing to file"""
        # First, add the values in this section stored directly in this class
        text_list = [Section.get_text(self)]
        if self.dates is not None:  # Add the values stored in Dates class
            text_list.append(self.dates.get_text().replace(self.SECTION_NAME + '\n', ''))
        if self.time_steps is not None:  # Add the values stored in TimeSteps class
            text_list.append(self.time_steps.get_text().replace(self.SECTION_NAME + '\n', ''))
        if self.dynamic_wave is not None:  # Add the values stored in DynamicWave class
            text_list.append(self.dynamic_wave.get_text().replace(self.SECTION_NAME + '\n', ''))
        return '\n'.join(text_list)

    def set_text(self, new_text):
        """Read this section from the text representation"""
        for line in new_text.splitlines():
            comment_split = str.split(line, ';', 1)
            if len(comment_split) == 2:
                line = comment_split[0]
                if self.comment:
                    self.comment += '\n'
                self.comment += ';' + comment_split[1]

            if not line.startswith('[') and line.strip():
                # Set fields from field_dict if this section has one
                tried_set = False
                for set_here in (self, self.dates, self.time_steps, self.dynamic_wave):
                    (attr_name, attr_value) = set_here.get_field_dict_value(line)
                    if attr_name:
                        try:
                            tried_set = True
                            set_here.setattr_keep_type(attr_name, attr_value)
                        except Exception as e:
                            print("options.General.text could not set " + attr_name + '\n' + str(e))
                if not tried_set:
                    print("options.General.text skipped: " + line)
