from enum import Enum
from core.coordinate import Coordinate, Polygon
from core.project_base import Section
from core.metadata import Metadata
from core.swmm.hydrology.raingage import RainGage


class Routing(Enum):
    """Routing of runoff between pervious and impervious areas
        IMPERV: runoff from pervious area flows to impervious area,
        PERV: runoff from impervious area flows to pervious area,
        OUTLET: runoff from both areas flows directly to outlet. """
    IMPERVIOUS = 1
    PERVIOUS = 2
    OUTLET = 3


class Subcatchment(Section, Polygon):
    """Subcatchment geometry, location, parameters, and time-series data"""


    #    attribute,         input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",                    '', "Name",            "",       '', '', "User-assigned name of subcatchment"),
        #("centroid.X",              '', "X-Coordinate",    "",       '', '', "X coordinate of subcatchment centroid on map"),
        #("centroid.Y",              '', "Y-Coordinate",    "",       '', '', "Y coordinate of subcatchment centroid on map"),
        ("description",             '', "Description",     "",       '', '', "Optional comment or description"),
        ("tag",                     '', "Tag",             "",       '', '', "Optional category or classification"),
        ("rain_gage",               '', "Rain Gage",       "*",      '', '', "Rain gage assigned to subcatchment"),
        ("outlet",                  '', "Outlet",          "*",      '', '', "Name of node or another subcatchment that receives runoff"),
        ("area",                    '', "Area",            "5",      '', '', "Area of subcatchment"),
        ("width",                   '', "Width",           "500",    '', '', "Width of overland flow path"),
        ("percent_slope",           '', "% Slope",         "0.5",    '', '', "Average surface slope"),
        ("percent_impervious",      '', "% Imperv",        "25",     '', '', "Percent of impervious area"),
        ("n_imperv",                '', "N-Imperv",        "0.01",   '', '', "Mannings N for impervious area"),
        ("n_perv",                  '', "N-Perv",          "0.1",    '', '', "Mannings N for pervious area"),
        ("storage_depth_imperv",    '', "Dstore-Imperv",   "0.05",   '', '', "Depth of depression storage on impervious area"),
        ("storage_depth_perv",      '', "Dstore-Perv",     "0.05",   '', '', "Depth of depression storage on pervious area"),
        ("percent_zero_impervious", '', "%Zero-Imperv",    "25",     '', '', "Percent of impervious area with no depression storage"),
        ("subarea_routing",         '', "Subarea Routing", "OUTLET", '', '', "Choice of internal routing between pervious and impervious sub-areas"),
        ("percent_routed",          '', "Percent Routed",  "100",    '', '', "Percent of runoff routed between sub-areas"),
        ("infiltration_parameters", '', "Infiltration",    "HORTON", '', '', "Infiltration parameters (click to edit)"),
        ("groundwater",             '', "Groundwater",     "NO",     '', '', "Groundwater flow parameters (click to edit)"),
        ("snow_pack",               '', "Snow Pack",       "",       '', '', "Name of snow pack parameter set (for snow melt analysis only)"),
        ("LIDUsage",                '', "LID Controls",    "0",      '', '', "LID controls (click to edit)"),
        ("coverages",               '', "Land Uses",       "0",      '', '', "Assignment of land uses to subcatchment (click to edit)"),
        ("initial_loadings",        '', "Initial Buildup", "NONE",   '', '', "Initial pollutant buildup on subcatchment (click to edit)"),
        ("curb_length",             '', "Curb Length",     "0",      '', '', "Curb length (if needed for pollutant buildup functions)")
    ))

    def __init__(self):
        Section.__init__(self)
        Polygon.__init__(self)

        ## Coordinates: Subcatchment's centroid on the Study Area Map.
        ## If not set, the subcatchment will not appear on the map.
        self.centroid = Coordinate()

        ## str: Optional description of the Subcatchment.
        self.description = ''

        ## Optional label used to categorize or classify the Subcatchment.
        self.tag = ''

        ## str: The RainGage ID associated with the Subcatchment.
        self.rain_gage = 'None'

        ## The Node or Subcatchment which receives Subcatchment's runoff.
        self.outlet = 'None'

        ## float: Area of the subcatchment (acres or hectares).
        self.area = 0.0

        ## float: Percent of land area which is impervious.
        self.percent_impervious = 0.0

        ## Characteristic width of the overland flow path for sheet flow
        ## runoff (feet or meters). An initial estimate of the characteristic
        ## width is given by the subcatchment area divided by the average
        ## maximum overland flow length. The maximum overland flow
        ## length is the length of the flow path from the the furthest drainage
        ## point of the subcatchment before the flow becomes channelized.
        ## Maximum lengths from several different possible flow paths
        ## should be averaged. These paths should reflect slow flow, such as
        ## over pervious surfaces, more than rapid flow over pavement, for
        ## example. Adjustments should be made to the width parameter to
        ## produce good fits to measured runoff hydrographs.
        self.width = 0.0

        ## float: Average percent slope of the subcatchment.
        self.percent_slope = 0.0

        ## float: Manning's n for overland flow in impervious part of Subcatchment
        self.n_imperv = 0.0

        ## Manning's n for overland flow in pervious part of Subcatchment
        self.n_perv = 0.0

        ## float: Depth of depression storage on the impervious portion of the
        ## Subcatchment (inches or millimeters)
        self.storage_depth_imperv = 0.0

        ## float: Depth of depression storage on the pervious portion of the
        ## Subcatchment (inches or millimeters)
        self.storage_depth_perv = 0.0

        ## float: Percent of the impervious area with no depression storage.
        self.percent_zero_impervious = 0.0

        ## Routing: Internal routing of runoff between pervious and impervious areas
        self.subarea_routing = Routing.OUTLET

        ## float: Percent of runoff routed between subareas
        self.percent_routed = 100.0

        ## infiltration parameters from horton, green-ampt, or scs classes
        self.infiltration_parameters = HortonInfiltration()
        #self.infiltration_parameters.subcatchment = self.name

        ## Snow pack parameter set (if any) of the subcatchment.
        self.snow_pack = ''

        ## Total length of curbs in the subcatchment (any length units).
        ## Used only when initial_loadings are normalized to curb length.
        self.curb_length = 0


class HortonInfiltration(Section):
    """Horton Infiltration parameters"""

    #    attribute,         input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("subcatchment",     '', "Subcatchment Name",  "", '', '', "User-assigned name of subcatchment"),
        ("max_rate",         '', "Max. Infil. Rate",   "", '', '', "Maximum rate on the Horton infiltration curve (in/hr or mm/hr)"),
        ("min_rate",         '', "Min. Infil. Rate",   "", '', '', "Minimum rate on the Horton infiltration curve (in/hr or mm/hr)"),
        ("decay",            '', "Decay Constant",     "", '', '', "Decay constant for the Horton infiltration curve (1/hr)"),
        ("dry_time",         '', "Drying Time",        "", '', '', "Time for a fully saturated soil to completely dry (days)"),
        ("max_volume",       '', "Max. Volume",        "", '', '', "Maximum infiltration volume possible (in or mm, 0 if not applicable)")
    ))

    def __init__(self):
        Section.__init__(self)

        ## Subcatchment name
        self.subcatchment = "None"

        ## Maximum infiltration rate on Horton curve (in/hr or mm/hr)
        self.max_rate = '0.0'

        ## Minimum infiltration rate on Horton curve (in/hr or mm/hr).
        self.min_rate = '0.0'

        ## Decay rate constant of Horton curve (1/hr).
        self.decay = '0.0'

        ## Time it takes for fully saturated soil to dry (days).
        self.dry_time = '0.0'

        ## Maximum infiltration volume possible (in or mm).
        self.max_volume = '0.0'


class GreenAmptInfiltration(Section):
    """Green-Ampt Infiltration parameters"""

    #    attribute,         input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("subcatchment",             '', "Subcatchment Name",  "", '', '', "User-assigned name of subcatchment"),
        ("suction",                  '', "Suction Head",       "", '', '', "Soil capillary suction head (in or mm)"),
        ("hydraulic_conductivity",   '', "Conductivity",       "", '', '', "Soil saturated hydraulic conductivity (in/hr or mm/hr)"),
        ("initial_moisture_deficit", '', "Initial Deficit",    "", '', '', "Difference between soil porosity and initial moisture content (a fraction)")
    ))

    def __init__(self):
        Section.__init__(self)

        ## Subcatchment name
        self.subcatchment = "None"

        ## Soil capillary suction (in or mm).
        self.suction = '0.0'

        ## Soil saturated hydraulic conductivity (in/hr or mm/hr).
        self.hydraulic_conductivity = '0.0'

        ## Initial soil moisture deficit (volume of voids / total volume).
        self.initial_moisture_deficit = '0.0'


class CurveNumberInfiltration(Section):
    """Curve Number Infiltration parameters"""

    #    attribute,         input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("subcatchment",             '', "Subcatchment Name",  "", '', '', "User-assigned name of subcatchment"),
        ("curve_number",             '', "Curve Number",       "", '', '', "SCS runoff curve number"),
        ("hydraulic_conductivity",   '', "Conductivity",       "", '', '', "This property has been deprecated and its value is ignored."),
        ("dry_days",                 '', "Drying Time",        "", '', '', "Time for a fully saturated soil to completely dry (days)")
    ))

    def __init__(self):
        Section.__init__(self)

        ## Subcatchment name
        self.subcatchment = "None"

        ## SCS Curve Number
        self.curve_number = "None"

        ## Soil saturated hydraulic conductivity (no longer used for curve number infiltration).
        self.hydraulic_conductivity = '0'

        ## Time it takes for fully saturated soil to dry (days).
        self.dry_days = '0.0'


class Groundwater(Section):
    """Link a subcatchment to an aquifer and to a drainage system node"""

    #    attribute,         input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("subcatchment",                        '', "Subcatchment Name",            "", '', '', "User-assigned name of subcatchment"),
        ("aquifer",                             '', "Aquifer Name",                 "", '', '', "Name of Aquifer object that lies below subcatchment. Leave blank for no groundwater."),
        ("receiving_node",                      '', "Receiving Node",               "", '', '', "Name of node that receives groundwater flow"),
        ("surface_elevation",                   '', "Surface Elevation",            "", '', '', "Elevation of the ground surface (ft or m)"),
        ("groundwater_flow_coefficient",        '', "A1 Coefficient",               "", '', '', "Groundwater influence multiplier."),
        ("groundwater_flow_exponent",           '', "B1 Exponent",                  "", '', '', "Groundwater influence exponent."),
        ("surface_water_flow_coefficient",      '', "A2 Coefficient",               "", '', '', "Tailwater influence multiplier."),
        ("surface_water_flow_exponent",         '', "B2 Exponent",                  "", '', '', "Tailwater influence exponent."),
        ("surface_gw_interaction_coefficient",  '', "A3 Coefficient",               "", '', '', "Combined groundwater/tailwater influence multiplier."),
        ("fixed_surface_water_depth",           '', "Surface Water Depth",          "", '', '', "Depth of surface water above channel bottom (ft or m). Enter 0 to use depth from flow routing."),
        ("threshold_groundwater_elevation",     '', "Threshold Water Table Elev.",  "", '', '', "Minimum water table elevation for flow to occur (ft or m). Leave blank to use node's invert elevation."),
        ("bottom_elevation",                    '', "Aquifer Bottom Elevation",     "", '', '', "Elevation of aquifer bottom (ft or m). Leave blank to use Aquifer value."),
        ("water_table_elevation",               '', "Initial Water Table Elev.",    "", '', '', "Initial water table elevation (ft or m). Leave blank to use Aquifer value."),
        ("unsaturated_zone_moisture",           '', "Unsat. Zone Moisture",         "", '', '', "Initial moisture content of the unsaturated upper zone (fraction). Leave blank to use Aquifer value."),
        ("custom_lateral_flow_equation",        '', "Custom Lateral Flow Equation", "", '', '', "Click to supply a custom equation for lateral GW flow."),
        ("custom_deep_flow_equation",           '', "Custom Deep Flow Equation",    "", '', '', "Click to supply a custom equation for deep GW flow.")
    ))

    def __init__(self):
        Section.__init__(self)

        ## Subcatchment name
        self.subcatchment = "None"

        ## Aquifer that supplies groundwater. None = no groundwater flow.
        self.aquifer = "None"

        ## Node that receives groundwater from the aquifer.
        self.receiving_node = "None"

        ## Elevation of ground surface for the subcatchment
        ## that lies above the aquifer (feet or meters).
        self.surface_elevation = '0.0'

        ## Value of A1 in the groundwater flow formula.
        self.groundwater_flow_coefficient = '0.0'

        ## Value of B1 in the groundwater flow formula.
        self.groundwater_flow_exponent = '0.0'

        ## Value of A2 in the groundwater flow formula.
        self.surface_water_flow_coefficient = '0.0'

        ## Value of B2 in the groundwater flow formula.
        self.surface_water_flow_exponent = '0.0'

        ## Value of A3 in the groundwater flow formula.
        self.surface_gw_interaction_coefficient = '0.0'

        ## Fixed depth of surface water at the receiving node (feet or meters)
        ## (set to zero if surface water depth will vary
        ## as computed by flow routing).
        ## This value is used to compute HSW.
        self.fixed_surface_water_depth = '0.0'

        ## Groundwater elevation that must be reached before any flow occurs
        ## (feet or meters).
        ## Leave blank to use the receiving node's invert elevation.
        self.threshold_groundwater_elevation = '*'

        ## override bottom elevation aquifer parameter
        self.bottom_elevation = ''

        ## override initial water table elevation aquifer parameter
        self.water_table_elevation = ''

        ## override initial upper moisture content aquifer parameter
        self.unsaturated_zone_moisture = ''

        ## expression for lateral groundwater flow (to a node of the conveyance network)
        self.custom_lateral_flow_equation = ''

        ## expression for vertical loss to deep groundwater
        self.custom_deep_flow_equation = ''


class LIDUsage(Section):
    """Specifies how an LID control will be deployed in a subcatchment"""

    def __init__(self):
        Section.__init__(self)

        ## Name of the Subcatchment defined in [SUBCATCHMENTS] where this usage occurs
        self.subcatchment_name = "None"

        ## Name of the LID control defined in [LID_CONTROLS] to be used in the subcatchment
        self.control_name = "None"

        ## Number of equal size units of the LID practice deployed within the subcatchment
        self.number_replicate_units = '0'

        ## Surface area devoted to each replicate LID unit
        self.area_each_unit = '0'

        ## Width of the outflow face of each identical LID unit
        self.top_width_overland_flow_surface = '0'

        ## Degree to which storage zone is initially filled with water
        self.percent_initially_saturated = '0'

        ## Percent of the impervious portion of the subcatchment's non-LID area whose runoff
        ## is treated by the LID practice
        self.percent_impervious_area_treated = '0'

        ## 1 if the outflow from the LID is returned onto the subcatchment's pervious area rather
        ## than going to the subcatchment's outlet
        self.send_outflow_pervious_area = '0'

        ## Name of an optional file where detailed time series results for the LID will be written
        self.detailed_report_file = ''

        ## ID of a subcatchment that this LID drains to
        self.subcatchment_drains_to = ''


class Coverage(Section):
    """Specifies the percentage of a subcatchments area that is covered by each category of land use."""

    def __init__(self, subcatchment_name = '', land_use_name = '', percent_subcatchment_area = ''):
        Section.__init__(self)

        ## Name of the Subcatchment defined in [SUBCATCHMENTS] where this coverage occurs
        self.subcatchment_name = subcatchment_name

        ## land use name from [LANDUSE] of this coverage
        self.land_use_name = land_use_name

        ## percent of subcatchment area covered by this land use
        self.percent_subcatchment_area = percent_subcatchment_area


class Coverages(Section):
    """Specifies the percentage of a subcatchments area that is covered by each category of land use."""

    SECTION_NAME = "[COVERAGES]"
    DEFAULT_COMMENT = ";;Subcatchment  \tLand Use        \tPercent\n"\
                      ";;--------------\t----------------\t----------"

    def __init__(self):
        Section.__init__(self)
        self.value = []


class InitialLoading(Section):
    """Specifies a pollutant buildup that exists on a subcatchment at the start of a simulation."""

    def __init__(self):
        Section.__init__(self)

        ## Name of the Subcatchment defined in [SUBCATCHMENTS] where this loading occurs
        self.subcatchment_name = "None"

        ## Name of a pollutant
        self.pollutant_name = "None"

        ## Initial buildup of pollutant (lbs/acre or kg/hectare)
        self.initial_buildup = '0'


class InitialLoadings(Section):
    """Specifies the pollutant buildup that exists on each subcatchment at the start of a simulation."""

    SECTION_NAME = "[LOADINGS]"
    DEFAULT_COMMENT = ";;Subcatchment  \tPollutant       \tBuildup\n"\
                      ";;--------------\t----------------\t----------"

    def __init__(self):
        Section.__init__(self)
        self.value = []
