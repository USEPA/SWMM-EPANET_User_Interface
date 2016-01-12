from enum import Enum

from core.coordinates import Coordinates
from core.swmm.groundwater import HortonInfiltration
from core.swmm.raingage import RainGage

class Routing(Enum):
    """Routing of runoff between pervious and impervious areas
        IMPERV: runoff from pervious area flows to impervious area,
        PERV: runoff from impervious area flows to pervious area,
        OUTLET: runoff from both areas flows directly to outlet. """
    IMPERV = 1
    PERV = 2
    OUTLET = 3


class Subcatchment:
    """Subcatchment geometry, location, parameters, and time-series data"""

    def __init__(self, name):
        self.name = name
        """str: User-assigned Subcatchment name."""

        self.description = None
        """str: Optional description of the Subcatchment."""

        self.tag = None
        """Optional label used to categorize or classify the Subcatchment."""

        self.polygon_vertices = []
        """List[Coordinates]:the Subcatchment's polygon."""

        self.centroid = Coordinates(None, None)
        """Coordinates: Subcatchment's centroid on the Study Area Map.
            If not set, the subcatchment will not appear on the map."""

        self.rain_gage = RainGage(None)
        """The RainGage associated with the Subcatchment."""

        self.outlet = None
        """The Node or Subcatchment which receives Subcatchment's runoff."""

        self.area = 0
        """Area of the subcatchment (acres or hectares)."""

        self.width = 0
        """Characteristic width of the overland flow path for sheet flow
            runoff (feet or meters). An initial estimate of the characteristic
            width is given by the subcatchment area divided by the average
            maximum overland flow length. The maximum overland flow
            length is the length of the flow path from the the furthest drainage
            point of the subcatchment before the flow becomes channelized.
            Maximum lengths from several different possible flow paths
            should be averaged. These paths should reflect slow flow, such as
            over pervious surfaces, more than rapid flow over pavement, for
            example. Adjustments should be made to the width parameter to
            produce good fits to measured runoff hydrographs."""

        self.percent_slope = 0
        """Average percent slope of the subcatchment."""

        self.percent_impervious = 0
        """Percent of land area which is impervious."""

        self.n_imperv = 0
        """Manning's n for overland flow in impervious part of Subcatchment"""

        self.n_perv = 0
        """Manning's n for overland flow in pervious part of Subcatchment"""

        self.storage_depth_imperv = 0
        """Depth of depression storage on the impervious portion of the
            Subcatchment (inches or millimeters) """

        self.storage_depth_perv = 0
        """Depth of depression storage on the pervious portion of the
            Subcatchment (inches or millimeters)"""

        self.percent_zero_impervious = 0
        """Percent of the impervious area with no depression storage."""

        self.subarea_routing = Routing.OUTLET
        """Internal routing of runoff between pervious and impervious areas"""

        self.percent_routed = 0
        """Percent of runoff routed between subareas"""

        self.infiltration = HortonInfiltration()
        """ Set to a fully specified HortonInfiltration,
            GreenAmptInfiltration or CurveNumberInfiltration."""

        self.lid_controls = {}
        """Low Impact Development controls in the Subcatchment."""

        self.groundwater = None
        """Groundwater flow parameters for the subcatchment."""

        self.snow_pack = None
        """Name of snow pack parameter set (if any) of the subcatchment."""

        self.coverages = {}
        """Land uses in the subcatchment."""

        self.initial_loadings = {}
        """Initial quantities of pollutant in the Subcatchment."""

        self.curb_length = 0
        """ Total length of curbs in the subcatchment (any length units).
            Used only when initial_loadings are normalized to curb length."""