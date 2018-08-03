# from traitlets import HasTraits, Int, Unicode
from enum import Enum
from core.coordinate import Coordinate
from core.project_base import Section
from core.metadata import Metadata


class Node(Section, Coordinate):
    """A node in a SWMM model (base class of Junction, Outfall, Divider, and Storage)"""
    def __init__(self):
        Coordinate.__init__(self)

        ## Unique name or number identifying this node
        # self.name, inherited from Coordinate

        ## Node location for mapping
        # self.x, self.y, inherited from Coordinate

        ## Optional description of the Node
        # self.description = ''

        ## Optional label used to categorize or classify this Node
        self.tag = ''
#
#         self.direct_inflows = []
#         """List of external direct, dry weather, or RDII inflows"""
#
#         self.dry_weather_inflows = []
#         """List of external direct, dry weather, or RDII inflows"""
#
#         self.rdi_inflows = []
#         """List of external direct, dry weather, or RDII inflows"""
#
#         self.treatments = []
#         """List of treatment functions for pollutants entering the node"""
#
#         self.invert_elev = ''
#         """Invert elevation of the Node (feet or meters)"""


class Junction(Node):
    """A Junction node"""

    #    attribute, input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",            '', "Name",            '',   '',   '', "User-assigned name of junction"),
        ('x',               '', "X-Coordinate",    '',   '',   '', "X coordinate of junction on study area map"),
        ('y',               '', "Y-Coordinate",    '',   '',   '', "Y coordinate of junction on study area map"),
        ('',                '', "Description",     '',   '',   '', "Optional comment or description"),
        ('tag',             '', "Tag",             '',   '',   '', "Optional category or classification"),
        ('',                '', "Inflows",         'NO', '',   '',
         "Click to specify any external inflows received at the junction"),
        ('.treatment(node_name)',                '', "Treatment",       'NO', '',   '',
         "Click to specify any pollutant removal supplied at the junction"),
        ("elevation",       '', "Invert El.",      '0', "(ft)",  "(m)", "Elevation of junction's invert"),
        ("max_depth",       '', "Max. Depth",      '0', "(ft)",  "(m)",
         "Maximum water depth (i.e. distance from invert to ground surface or 0 to use distance "
         "from invert to top of highest connecting link)"),
        ("initial_depth",   '', "Initial Depth",   '0', "(ft)",  "(m)",
         "Initial water depth in junction"),
        ("surcharge_depth", '', "Surcharge Depth", '0', "(ft)",  "(m)",
         "Depth in excess of maximum depth before flooding occurs"),
        ("ponded_area",     '', "Ponded Area",     '0', "(ft2)", "(m2)", "Area of ponded water when flooded")))

    def __init__(self):
        Node.__init__(self)

        # self.name = ''  # Unicode(default_value='', label="Name", help="User-assigned name of junction")
        # """name assigned to junction node"""

        ## Invert elevation of the Node (feet or meters)
        self.elevation = 0.0

        ## Maximum depth of junction (i.e., from ground surface to invert)
        ## feet or meters). If zero, then the distance from the invert to
        ## the top of the highest connecting link will be used.  (Ymax)
        self.max_depth = 0.0

        ## Depth of water at the junction at the start of the simulation
        ## (feet or meters) (Y0)
        self.initial_depth = 0.0

        ## Additional depth of water beyond the maximum depth that is
        ##  allowed before the junction floods (feet or meters).
        ## This parameter can be used to simulate bolted manhole covers
        ## or force main connections. (Ysur)
        self.surcharge_depth = 0.0

        ## Area occupied by ponded water atop the junction after flooding
        ## occurs (sq. feet or sq. meters). If the Allow Ponding simulation
        ## option is turned on, a non-zero value of this parameter will allow
        ## ponded water to be stored and subsequently returned to the
        ## conveyance system when capacity exists. (Apond)
        self.ponded_area = 0.0


class OutfallType(Enum):
    """Type of outfall boundary condition:
        FREE: outfall stage determined by minimum of critical flow
                depth and normal flow depth in the connecting conduit
        NORMAL: outfall stage based on normal flow depth in
                connecting conduit
        FIXED: outfall stage set to a fixed value
        TIDAL: outfall stage given by a table of tide elevation versus
                time of day
        TIMESERIES: outfall stage supplied from a time series of elevations.
    """
    FREE = 1
    NORMAL = 2
    FIXED = 3
    TIDAL = 4
    TIMESERIES = 5


class Outfall(Junction):
    """A terminal node of the drainage system
        Defines a final downstream boundary under Dynamic Wave flow routing.
        For other types of flow routing they behave as a junction.
        Only a single link can be connected to an outfall node.
        The boundary conditions at an outfall can be described by any one
        of the following stage relationships:
            the critical or normal flow depth in the connecting conduit
            a fixed stage elevation
            a tidal stage described in a table of tide height versus hour
            a user-defined time series of stage versus time.
        The principal input parameters for outfalls include:
            invert elevation
            boundary condition type and stage description
            presence of a flap gate to prevent backflow through the outfall.
    """

    #    attribute, input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",                '', "Name",            '',   '',   '',      "User-assigned name of outfall"),
        ('x',                   '', "X-Coordinate",    '',   '',   '',      "X coordinate of outfall on study area map"),
        ('y',                   '', "Y-Coordinate",    '',   '',   '',      "Y coordinate of outfall on study area map"),
       #('',                    '', "Description",     '',   '',   '',      "Optional comment or description"),
        ('tag',                 '', "Tag",             '',   '',   '',      "Optional category or classification"),
        ('',                    '', "Inflows",         'NO', '',   '',      "Click to specify any external inflows received at the outfall"),
        ('.treatment(name)',    '', "Treatment",       'NO', '',   '',      "Click to specify any pollutant removal supplied at the outfall"),
        ("elevation",           '', "Invert El.",      '0',  "(ft)", "(m)", "Elevation of outfall's invert"),
        ("tide_gate",           '', "Tide Gate",       '0',  '',   '',      "True if outfall contains a tide gate to prevent backflow"),
        ("route_to",            '', "Route To",        '',   '',   '',      "Subcatchment outfall is routed onto (blank if not applicable)"),
        ("outfall_type",        '', "Type",            '0',  '',   '',      "Type of outfall boundary condition"),
        ("fixed_stage",         '', "Fixed Stage",     '0',  '(ft)', '(m)', "Water elevation for a FIXED boundary condition"),
        ("tidal_curve",         '', "Curve Name",      '0',  '',   '',      "Name of tidal curve used for a TIDAL boundary condition"),
        ("time_series_name",    '', "Series Name",     '0',  '',   '',      "Name of time series for a TIMESERIES boundary condition")))

    def __init__(self):
        Junction.__init__(self)

        ## Tide Gate is present to prevent backflow
        self.tide_gate = False

        ## Type of outfall boundary condition
        self.outfall_type = OutfallType.FREE

        ## Water elevation for a FIXED type of outfall (feet or meters).
        self.fixed_stage = 0.0

        ## The TidalCurve relating water elevation to hour of the
        ## day for a TIDAL outfall.
        self.tidal_curve = "None"

        ## Name of time series containing time history of outfall elevations
        ## for a TIMESERIES outfall
        self.time_series_name = "None"

        ## Optional name of a subcatchment that receives the outfall's discharge
        self.route_to = ''


class FlowDividerType(Enum):
    """Type of flow divider. Choices are:
        CUTOFF (diverts all inflow above a defined cutoff value),
        OVERFLOW (diverts all inflow above the flow capacity of the
                non-diverted link),
        TABULAR (uses a Diversion Curve to express diverted flow as a
                function of the total inflow),
        WEIR (uses a weir equation to compute diverted flow).
    """
    CUTOFF = 1
    OVERFLOW = 2
    TABULAR = 3
    WEIR = 4


class WeirDivider:
    def __init__(self):
        ## Minimum flow at which diversion begins (flow units).
        self.min_flow = 0.0

        ## Vertical height of WEIR opening (feet or meters)
        self.max_depth = 0.0

        ## Product of WEIR's discharge coefficient and its length.
        ## Weir coefficients are typically in the range of
        ## 2.65 to 3.10 per foot, for flows in CFS.
        self.coefficient = 0.0


class Divider(Junction):
    """Flow Dividers are drainage system nodes that divert inflows to
        a specific conduit in a prescribed manner. A flow divider can
        have no more than two conduit links on its discharge side.
        Flow dividers are only active under Kinematic Wave routing
        and are treated as simple junctions under Dynamic Wave routing.
    """

    #    attribute, input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",                '', "Name",            '',   '',   '',        "User-assigned name of divider"),
        ('x',                   '', "X-Coordinate",    '',   '',   '',        "X coordinate of divider on study area map"),
        ('y',                   '', "Y-Coordinate",    '',   '',   '',        "Y coordinate of divider on study area map"),
        ('',                    '', "Description",     '',   '',   '',        "Optional comment or description"),
        ('tag',                 '', "Tag",             '',   '',   '',        "Optional category or classification"),
        ('',                    '', "Inflows",         'NO', '',   '',        "Click to specify any external inflows received at the divider"),
        ('.treatment(node_name)', '', "Treatment",   'NO', '',   '',          "Click to specify any pollutant removal supplied at the divider"),
        ("elevation",           '', "Invert El.",      '0',  "(ft)", "(m)",   "Elevation of divider's invert"),
        ("max_depth",           '', "Max Depth",       '0',  '(ft)', '(m)',
         "Maximum water depth (distance from invert to ground) or 0 to use distance from invert to top of highest connecting link"),
        ("initial_depth",       '', "Initial Depth",   '0',  '(ft)', '(m)',   "Initial water depth in junction"),
        ("surcharge_depth",     '', "Surcharge Depth", '0',  '(ft)', '(m)',   "Depth in excess of maximum depth before flooding occurs"),
        ("ponded_area",         '', "Ponded Area",     '0',  '(ft2)', '(m2)', "Area of ponded water when flooded"),
        ("diverted_link",       '', "Diverted Link",   '',   '',   '',        "Name of link which receives the diverted flow"),
        ("flow_divider_type",   '', "Type",            '',   '',   '',        "Type of flow divider"),
        ("min_diversion_flow",  '', "Diversion Flow",  '0',  '',   '',        "Minimum flow at which diversion begins"),
        ("divider_curve",       '', "Tabular Curve Name", '', '',  '',        "Name of diversion curve used with a TABULAR divider"),
        ("weir_height",         '', "Weir Height",      '0',  '(ft)', '(m)',  "Depth at maximum flow for a WEIR divider"),
        ("weir_coefficient",    '', "Weir Coefficient", '0',  '',  '',        "Discharge coefficient for a WEIR divider")))

    def __init__(self):
        Junction.__init__(self)

        ## Name of link which receives the diverted flow.
        self.diverted_link = "None"

        ## Type of flow divider from FlowDividerType(Enum)
        self.flow_divider_type = FlowDividerType.CUTOFF

        ## Flow at which diversion begins for a CUTOFF or WEIR divider (flow units).
        self.min_diversion_flow = 0.0

        ## Diversion Curve used with a TABULAR divider
        self.divider_curve = "None"

        ## Height of WEIR divider (ft or m)
        self.weir_height = 0.0

        ## Discharge coefficient for a WEIR divider
        self.weir_coefficient = 0.0


class StorageCurveType(Enum):
    FUNCTIONAL = 1
    TABULAR = 2


class StorageUnit(Junction):
    """Storage Units are drainage system nodes that provide storage volume.
        Physically they could represent storage facilities as small as
        a catch basin or as large as a lake. The volumetric properties
        of a storage unit are described by a function or table of
        surface area versus height.
    """

    #    attribute, input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",                '', "Name",            '',   '',   '',      "User-assigned name of storage unit"),
        ('x',                   '', "X-Coordinate",    '',   '',   '',      "X coordinate of storage unit on study area map"),
        ('y',                   '', "Y-Coordinate",    '',   '',   '',      "Y coordinate of storage unit on study area map"),
        ('',                    '', "Description",     '',   '',   '',      "Optional comment or description"),
        ('tag',                 '', "Tag",             '',   '',   '',      "Optional category or classification"),
        ('',                    '', "Inflows",         'NO', '',   '',      "Click to specify any external inflows received at the storage unit"),
        ('.treatment(node_name)', '', "Treatment",     'NO', '',   '',      "Click to specify any pollutant removal supplied at the storage unit"),
        ("elevation",           '', "Invert El.",      '0',  '(ft)', '(m)', "Elevation at the bottom of the storage unit"),
        ("max_depth",           '', "Max Depth",       '0',  '(ft)', '(m)', "Maximum depth of the storage unit"),
        ("initial_depth",       '', "Initial Depth",   '0',  '(ft)', '(m)', "Initial depth of water in the storage unit"),
        ("evaporation_factor",  '', "Evap. Factor",    '',   '',   '',      "Fraction of evaporation rate realized"),
        ("seepage_loss",        '', "Seepage Loss",    'NO', '',   '',      "Click to specify soil properties that determine seepage loss through the bottom and sloped sides of the storage unit"),
        ("storage_curve_type",  '', "Storage Curve",   '0',  '',   '',      "Method of describing the geometric shape of the storage unit"),
        ("coefficient",         '', "Functional Curve Coefficient",   '',   '(ft)', '(m)',  "A-value in expression Area = A*Depth^B + C"),
        ("exponent",            '', "Functional Curve Exponent",      '0',  '(ft)', '(m)',  "B-value in expression Area = A*Depth^B + C"),
        ("constant",            '', "Functional Curve Constant",      '0',  '(ft)', '(m)',  "C-value in expression Area = A*Depth^B + C"),
        ("storage_curve",       '', "Tabular Curve Name",             '0',  '',   '',  "Name of storage curve to use")))

    def __init__(self):
        Junction.__init__(self)

        ## StorageCurveType: FUNCTIONAL or TABULAR
        self.storage_curve_type = StorageCurveType.TABULAR

        ## Storage Curve containing the relationship between
        ## surface area and storage depth
        self.storage_curve = "None"

        ## A-value in the functional relationship
        ## between surface area and storage depth.
        self.coefficient = '0'

        ## B-value in the functional relationship
        ## between surface area and storage depth.
        self.exponent = '0'

        ## C-value in the functional relationship
        ## between surface area and storage depth.
        self.constant = '0'

        ## The fraction of the potential evaporation from the storage units
        ## water surface that is actually realized.
        self.evaporation_factor = '0'

        ## The following Green-Ampt infiltration parameters are only used when the storage
        ## node is intended to act as an infiltration basin
        self.seepage_loss = '0'

        ## Soil capillary suction head (in or mm)
        self.seepage_suction_head = '0'

        ## Soil saturated hydraulic conductivity (in/hr or mm/hr)
        self.seepage_hydraulic_conductivity = '0'

        ## Initial soil moisture deficit (volume of voids / total volume)
        self.seepage_initial_moisture_deficit = '0'


class DirectInflowType(Enum):
    CONCEN = 1
    MASS = 2


class DirectInflow(Section):
    """Defines characteristics of inflows added directly into a node"""

    def __init__(self):
        Section.__init__(self)

        ## str: name of node where external inflow enters
        self.node = "None"

        ## str: Name of the time series describing how flow or constituent loading to this node varies with time
        self.timeseries = "None"

        ## str: Name of constituent (pollutant) or FLOW
        self.constituent = "FLOW"

        ## DirectInflowType: Type of data contained in constituent_timeseries, concentration or mass flow rate
        self.format = DirectInflowType.CONCEN

        ## float: Numerical factor used to convert the units of pollutant mass flow rate in constituent_timeseries
        ## into project mass units per second as specified in [POLLUTANTS]
        self.conversion_factor = '1.0'

        ## float: Scaling factor that multiplies the recorded time series values
        self.scale_factor = '1.0'

        ## float: Constant baseline added to the time series values
        self.baseline = '0.0'

        ## str: ID of Time Pattern whose factors adjust the baseline inflow on an hourly, daily, or monthly basis
        self.baseline_pattern = ''

        ## pattern object
        self.baseline_pattern_object = None


class DryWeatherInflow(Section):
    """Specifies dry weather flow and its quality entering the drainage system at a specific node"""

    def __init__(self):
        Section.__init__(self)

        ## str: name of node where external inflow enters
        self.node = "None"

        ## str: Name of constituent (pollutant) or FLOW
        self.constituent = "FLOW"

        ## str: Average (or baseline) value of the dry weather inflow of the constituent in the relevant units
        self.average = '0.0'

        ## str: ID of time pattern used to allow the dry weather flow to vary in a periodic fashion
        self.time_patterns = []

        ## pattern object list
        self.time_pattern_objects = []


class RDIInflow(Section):
    """Defines characteristics of Rainfall-Dependent Infiltration/Inflows entering the system at a node"""

    def __init__(self):
        Section.__init__(self)

        ## str: name of node where external inflow enters
        self.node = ''

        ## str: name of an RDII unit hydrograph group specified in the [HYDROGRAPHS] section
        self.hydrograph_group = "None"

        ## float: area of the sewershed which contributes RDII to the node (acres or hectares)
        self.sewershed_area = '0'


class Treatment(Section):
    """Define the treatment properties of a node using a treatment expression"""

    hint = "Treatment expressions have the general form:\n" \
           "  R = f(P, R_P, V)\n" \
           "or\n" \
           "  C = f(P, R_P, V)\n" \
           "where:\n" \
           "  R   = fractional removal,\n" \
           "  C   = outlet concentration,\n" \
           "  P   = one or more pollutant names,\n" \
           "  R_P = one or more pollutant removals\n" \
           "        (prepend R_ to pollutant name),\n" \
           "  V   = one or more process variables:\n" \
           "        FLOW (inflow rate)\n" \
           "        DEPTH (water depth)\n" \
           "        HRT (hydraulic residence time)\n" \
           "        DT (time step in seconds)\n" \
           "        AREA (surface area).\n" \
           "Some example expressions are:\n" \
           "  C = BOD * exp(-0.05*HRT)\n" \
           "  R = 0.75 * R_TSS"

    #    attribute, input_name, label,             default, english, metric, hint
    metadata = Metadata((
        ("pollutant",       '', "Pollutant",            '',  '',         '', hint),
        ("function",        '', "Treatment Expression", '',  '',         '', hint)))

    def __init__(self):
        Section.__init__(self)

        ## str: name of node where external inflow enters.
        self.node = "None"

        ## Name of pollutant receiving treatment
        self.pollutant = "None"

        ## str: mathematical function expressing treatment result in terms of pollutant concentrations,
        ## pollutant removals, and other standard variables. Starts with C for concentration or R for removal.
        self.function = ''


class SubCentroid(Node):
    """Centroid for Subcatchment, as a node"""

    #    attribute, input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",            '', "Name",            '',   '',   '', "The subcatchment's name of centroid"),
        ('x',               '', "X-Coordinate",    '',   '',   '', "X coordinate of junction on study area map"),
        ('y',               '', "Y-Coordinate",    '',   '',   '', "Y coordinate of junction on study area map"),
        ('subname',         '', "Sub name",        '',   '',   '', "Subcatchment name"),
        ('tag',             '', "Tag",             '',   '',   '', "Optional category or classification"),
        ('',                '', "Inflows",         'NO', '',   '',
         "Click to specify any external inflows received at the junction")))

    def __init__(self):
        Node.__init__(self)
        pass
