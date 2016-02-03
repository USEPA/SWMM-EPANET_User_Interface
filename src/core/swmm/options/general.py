from enum import Enum

import core.inputfile
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


class General(core.inputfile.Section):
    """SWMM General Options"""

    SECTION_NAME = "[OPTIONS]"

    # @staticmethod
    # def default():
    #     return Options(Options.SECTION_NAME, None, None, -1)

    def __init__(self):
        core.inputfile.Section.__init__(self)
        # TODO: parse "value" argument to extract values for each field, after setting default values below

        self.flow_units = FlowUnits.CFS
        """FlowUnits: units in use for flow values"""

        self.infiltration = core.swmm.hydrology.subcatchment.HortonInfiltration()
        """
        Infiltration computation model of rainfall into the 
        upper soil zone of subcatchments. Use one of the following:
        HortonInfiltration, GreenAmptInfiltration, or CurveNumberInfiltration
        """

        self.flow_routing = FlowRouting.STEADY
        """Method used to route flows through the drainage system"""

        self.link_offsets = LinkOffsets.DEPTH
        """
        Convention used to specify the position of a link offset
        above the invert of its connecting node
        """

        self.ignore_rainfall = False
        """True to ignore all rainfall data and runoff calculations"""

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
