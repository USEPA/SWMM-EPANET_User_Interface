from enum import Enum
from core.coordinates import Coordinates
from core.inputfile import Section
from core.swmm.hydrology.raingage import RainGage


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

        self.centroid = Coordinates(None, None)
        """Coordinates: Subcatchment's centroid on the Study Area Map.
            If not set, the subcatchment will not appear on the map."""

        self.polygon_vertices = []
        """List[Coordinates]:the Subcatchment's polygon."""

        self.description = None
        """str: Optional description of the Subcatchment."""

        self.tag = None
        """Optional label used to categorize or classify the Subcatchment."""

        self.rain_gage = ""
        """str: The RainGage ID associated with the Subcatchment."""

        self.outlet = None
        """The Node or Subcatchment which receives Subcatchment's runoff."""

        self.area = 0.0
        """float: Area of the subcatchment (acres or hectares)."""

        self.percent_impervious = 0
        """float: Percent of land area which is impervious."""

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
        """float: Average percent slope of the subcatchment."""

        self.n_imperv = 0
        """float: Manning's n for overland flow in impervious part of Subcatchment"""

        self.n_perv = 0
        """Manning's n for overland flow in pervious part of Subcatchment"""

        self.storage_depth_imperv = 0
        """float: Depth of depression storage on the impervious portion of the
            Subcatchment (inches or millimeters) """

        self.storage_depth_perv = 0
        """float: Depth of depression storage on the pervious portion of the
            Subcatchment (inches or millimeters)"""

        self.percent_zero_impervious = 0
        """float: Percent of the impervious area with no depression storage."""

        self.subarea_routing = Routing.OUTLET
        """Routing: Internal routing of runoff between pervious and impervious areas"""

        self.percent_routed = 0
        """float: Percent of runoff routed between subareas"""

        self.infiltration_parameters = HortonInfiltration()
        """infiltration parameters from horton, green-ampt, or scs classes"""

        self.groundwater = None
        """Groundwater flow parameters for the subcatchment."""

        self.snow_pack = None
        """Snow pack parameter set (if any) of the subcatchment."""

        self.coverages = {}
        """Land uses in the subcatchment."""

        self.initial_loadings = {}
        """Initial quantities of pollutant in the Subcatchment."""

        self.curb_length = 0
        """ Total length of curbs in the subcatchment (any length units).
            Used only when initial_loadings are normalized to curb length."""


class HortonInfiltration:
    """Horton Infiltration parameters"""
    def __init__(self):
        self.max_rate = 0.0
        """Maximum infiltration rate on Horton curve (in/hr or mm/hr)"""

        self.min_rate = 0.0
        """Minimum infiltration rate on Horton curve (in/hr or mm/hr)."""

        self.decay = 0.0
        """Decay rate constant of Horton curve (1/hr)."""

        self.dry_time = 0.0
        """Time it takes for fully saturated soil to dry (days)."""

        self.max_volume = 0.0
        """Maximum infiltration volume possible (in or mm)."""


class GreenAmptInfiltration:
    """Green-Ampt Infiltration parameters"""
    def __init__(self):
        self.suction = 0.0
        """Soil capillary suction (in or mm)."""

        self.hydraulic_conductivity = 0.0
        """Soil saturated hydraulic conductivity (in/hr or mm/hr)."""

        self.initial_moisture_deficit = 0.0
        """Initial soil moisture deficit (volume of voids / total volume)."""


class CurveNumberInfiltration:
    """Curve Number Infiltration parameters"""
    def __init__(self):
        self.curve_number = None
        """SCS Curve Number"""

        self.dry_days = 0
        """Time it takes for fully saturated soil to dry (days)."""


class Groundwater:
    """Link a subcatchment to an aquifer and to a drainage system node"""

    def __init__(self, aquifer, receiving_node):
        self.aquifer = aquifer
        """Aquifer that supplies groundwater. None = no groundwater flow."""

        self.receiving_node = receiving_node
        """Node that receives groundwater from the aquifer."""

        self.surface_elevation = 0.0
        """Elevation of ground surface for the subcatchment
            that lies above the aquifer (feet or meters)."""

        self.groundwater_flow_coefficient = 0.0
        """Value of A1 in the groundwater flow formula."""

        self.groundwater_flow_exponent = 0.0
        """Value of B1 in the groundwater flow formula."""

        self.surface_water_flow_coefficient = 0.0
        """Value of A2 in the groundwater flow formula."""

        self.surface_water_flow_exponent = 0.0
        """Value of B2 in the groundwater flow formula."""

        self.surface_gw_interaction_coefficient = 0.0
        """Value of A3 in the groundwater flow formula."""

        self.fixed_surface_water_depth = 0.0
        """Fixed depth of surface water at the receiving node (feet or meters)
            (set to zero if surface water depth will vary
             as computed by flow routing).
            This value is used to compute HSW."""

        self.threshold_groundwater_elevation = 0.0
        """Groundwater elevation that must be reached before any flow occurs
            (feet or meters).
            Leave blank to use the receiving node's invert elevation."""


class LIDUsage(Section):
    """Specifies how an LID control will be deployed in a subcatchment"""

    field_format = " {:15}\t{:16}\t{:7}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}\t{:24}"  # TODO: add fields? \t{:24}\t{:16}

    def __init__(self, new_text=None):
        Section.__init__(self)
        self.subcatchment_name = ''
        """Name of the Subcatchment defined in [SUBCATCHMENTS] where this usage occurs"""

        self.control_name = ''
        """Name of the LID control defined in [LID_CONTROLS] to be used in the subcatchment"""

        self.number_replicate_units = '0'
        """Number of equal size units of the LID practice deployed within the subcatchment"""

        self.area_each_unit = '0.0'
        """Surface area devoted to each replicate LID unit"""

        self.top_width_overland_flow_surface = '0.0'
        """Width of the outflow face of each identical LID unit"""

        self.percent_initially_saturated = '0.0'
        """Degree to which storage zone is initially filled with water"""

        self.percent_impervious_area_treated = '0.0'
        """Percent of the impervious portion of the subcatchment's non-LID area whose runoff
        is treated by the LID practice"""

        self.send_outflow_pervious_area = '0'
        """1 if the outflow from the LID is returned onto the subcatchment's pervious area rather
        than going to the subcatchment's outlet"""

        self.detailed_report_file = ""
        """Name of an optional file where detailed time series results for the LID will be written"""

        if new_text:
            self.set_text(new_text)

    def get_text(self):
        inp = ''
        if self.comment:
            inp = self.comment + '\n'
        inp += LIDUsage.field_format.format(self.subcatchment_name,
                                            self.control_name,
                                            self.number_replicate_units,
                                            self.area_each_unit,
                                            self.top_width_overland_flow_surface,
                                            self.percent_initially_saturated,
                                            self.percent_impervious_area_treated,
                                            self.send_outflow_pervious_area,
                                            self.detailed_report_file)
        return inp

    def set_text(self, new_text):
        self.__init__()
        fields = new_text.split()
        if len(fields) > 0:
            self.subcatchment_name = fields[0]
        if len(fields) > 1:
            self.control_name = fields[1]
        if len(fields) > 2:
            self.number_replicate_units = fields[2]
        if len(fields) > 3:
            self.area_each_unit = fields[3]
        if len(fields) > 4:
            self.top_width_overland_flow_surface = fields[4]
        if len(fields) > 5:
            self.percent_initially_saturated = fields[5]
        if len(fields) > 6:
            self.percent_impervious_area_treated = fields[6]
        if len(fields) > 7:
            self.send_outflow_pervious_area = fields[7]
        if len(fields) > 8:
            self.detailed_report_file = fields[8]


class Coverage:
    """Specifies the percentage of a subcatchments area that is covered by each category of land use."""
    def __init__(self):
        self.land_use_name = ""
        """land use name"""

        self.percent_subcatchment_area = 0
        """percent of subcatchment area"""


class InitialLoading:
    """Specifies the pollutant buildup that exists on each subcatchment at the start of a simulation."""
    def __init__(self):
        self.pollutant_name = ""
        """name of a pollutant"""

        self.initial_buildup = 0
        """initial buildup of pollutant (lbs/acre or kg/hectare)"""
