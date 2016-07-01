from enum import Enum
from core.coordinates import Coordinates
from core.inputfile import Section
from core.metadata import Metadata


# class Node(object):
#     """A node in a SWMM model"""
#     def __init__(self):
#         self.node_id = ''
#         """Node Name"""
#
#         self.centroid = Coordinates(0.0, 0.0)
#         """Coordinates of Node location (x, y)"""
#
#         self.description = ''
#         """Optional description of the Node"""
#
#         self.tag = ''
#         """Optional label used to categorize or classify the Node"""
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


class Junction(Section):
    """A Junction node"""

    field_format = "{:16}\t{:10}\t{:10}\t{:10}\t{:10}\t{}"

    #    attribute, input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",            '', "Name",            '',   '',   '', "User-assigned name of junction"),
        ('',                '', "X-Coordinate",    '',   '',   '', "X coordinate of junction on study area map"),
        ('',                '', "Y-Coordinate",    '',   '',   '', "Y coordinate of junction on study area map"),
        ('',                '', "Description",     '',   '',   '', "Optional comment or description"),
        ('',                '', "Tag",             '',   '',   '', "Optional category or classification"),
        ('',                '', "Inflows",         'NO', '',   '',
         "Click to specify any external inflows received at the junction"),
        ('.treatment(node_id)',                '', "Treatment",       'NO', '',   '',
         "Click to specify any pollutant removal supplied at the junction"),
        ("elevation",       '', "Invert El.",      '0', "ft",  "m", "Elevation of junction's invert"),
        ("max_depth",       '', "Max. Depth",      '0', "ft",  "m",
         "Maximum water depth (i.e. distance from invert to ground surface or 0 to use distance "
         "from invert to top of highest connecting link)"),
        ("initial_depth",   '', "Initial Depth",   '0', "ft",  "m",
         "Initial water depth in junction"),
        ("surcharge_depth", '', "Surcharge Depth", '0', "ft",  "m",
         "Depth in excess of maximum depth before flooding occurs"),
        ("ponded_area",     '', "Ponded Area",     '0', "ft2", "m2", "Area of ponded water when flooded")))

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            Section.__init__(self)

            self.name = ''
            """name assigned to junction node"""

            self.elevation = ''
            """Invert elevation of the Node (feet or meters)"""

            self.max_depth = ''
            """Maximum depth of junction (i.e., from ground surface to invert)
                (feet or meters). If zero, then the distance from the invert to
                the top of the highest connecting link will be used.  (Ymax)"""

            self.initial_depth = ''
            """Depth of water at the junction at the start of the simulation
                (feet or meters) (Y0)"""

            self.surcharge_depth = ''
            """Additional depth of water beyond the maximum depth that is
                allowed before the junction floods (feet or meters).
                This parameter can be used to simulate bolted manhole covers
                or force main connections. (Ysur)"""

            self.ponded_area = ''
            """Area occupied by ponded water atop the junction after flooding
                occurs (sq. feet or sq. meters). If the Allow Ponding simulation
                option is turned on, a non-zero value of this parameter will allow
                ponded water to be stored and subsequently returned to the
                conveyance system when capacity exists. (Apond)"""

    def get_text(self):
        """format contents of this item for writing to file"""
        return self.field_format.format(self.name, self.elevation,
                                        self.max_depth, self.initial_depth, self.surcharge_depth, self.ponded_area)

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 0:
            self.name = fields[0]
        if len(fields) > 1:
            self.elevation = fields[1]
        if len(fields) > 2:
            self.max_depth = fields[2]
        if len(fields) > 3:
            self.initial_depth = fields[3]
        if len(fields) > 4:
            self.surcharge_depth = fields[4]
        if len(fields) > 5:
            self.ponded_area = fields[5]


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


class Outfall(Section):
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
    field_format = "{:16}\t{:10}\t{:10}\t{:16}\t{:8}\t{:16}\t{}"

    #    attribute, input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",                '', "Name",            '',   '',   '',  "User-assigned name of outfall"),
        ('',                    '', "X-Coordinate",    '',   '',   '',  "X coordinate of outfall on study area map"),
        ('',                    '', "Y-Coordinate",    '',   '',   '',  "Y coordinate of outfall on study area map"),
        ('',                    '', "Description",     '',   '',   '',  "Optional comment or description"),
        ('',                    '', "Tag",             '',   '',   '',  "Optional category or classification"),
        ('',                    '', "Inflows",         'NO', '',   '',  "Click to specify any external inflows received at the outfall"),
        ('.treatment(node_id)', '', "Treatment",       'NO', '',   '',  "Click to specify any pollutant removal supplied at the outfall"),
        ("elevation",           '', "Invert El.",      '0',  "ft", "m", "Elevation of outfall's invert"),
        ("tide_gate",           '', "Tide Gate",       '0',  '',   '',  "True if outfall contains a tide gate to prevent backflow"),
        ("route_to",            '', "Route To",        '0',  '',   '',  "Subcatchment outfall is routed onto (blank if not applicable)"),
        ("outfall_type",        '', "Type",            '0',  '',   '',  "Type of outfall boundary condition"),
        ("fixed_stage",         '', "Fixed Stage",     '0',  '',   '',  "Water elevation for a FIXED boundary condition"),
        ("tidal_curve",         '', "Curve Name",      '0',  '',   '',  "Name of tidal curve used for a TIDAL boundary condition"),
        ("time_series_name",    '', "Series Name",     '0',  '',   '',  "Name of time series for a TIMESERIES boundary condition")))

    def __init__(self):
        Section.__init__(self)

        self.tide_gate = False
        """Tide Gate is present to prevent backflow"""

        self.outfall_type = OutfallType.FREE
        """Type of outfall boundary condition"""

        self.fixed_stage = 0.0
        """Water elevation for a FIXED type of outfall (feet or meters)."""

        self.tidal_curve = None
        """The TidalCurve relating water elevation to hour of the
            day for a TIDAL outfall."""

        self.time_series_name = None
        """Name of time series containing time history of outfall elevations
            for a TIMESERIES outfall"""

        self.route_to = None
        """Optional name of a subcatchment that receives the outfall's discharge"""


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
        self.min_flow = 0.0
        """Minimum flow at which diversion begins (flow units)."""

        self.max_depth = 0.0
        """Vertical height of WEIR opening (feet or meters)"""

        self.coefficient = 0.0
        """Product of WEIR's discharge coefficient and its length.
            Weir coefficients are typically in the range of
            2.65 to 3.10 per foot, for flows in CFS."""


class Divider(Junction):
    """Flow Dividers are drainage system nodes that divert inflows to
        a specific conduit in a prescribed manner. A flow divider can
        have no more than two conduit links on its discharge side.
        Flow dividers are only active under Kinematic Wave routing
        and are treated as simple junctions under Dynamic Wave routing.
    """
    field_format = "{:16}\t{:10}\t{:10}\t{:16}\t{:8}\t{:16}\t{}"

    #    attribute, input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",                '', "Name",            '',   '',   '',  "User-assigned name of divider"),
        ('',                    '', "X-Coordinate",    '',   '',   '',  "X coordinate of divider on study area map"),
        ('',                    '', "Y-Coordinate",    '',   '',   '',  "Y coordinate of divider on study area map"),
        ('',                    '', "Description",     '',   '',   '',  "Optional comment or description"),
        ('',                    '', "Tag",             '',   '',   '',  "Optional category or classification"),
        ('',                    '', "Inflows",         'NO', '',   '',  "Click to specify any external inflows received at the divider"),
        ('.treatment(node_id)', '', "Treatment",       'NO', '',   '',  "Click to specify any pollutant removal supplied at the divider"),
        ("elevation",           '', "Invert El.",      '0',  "ft", "m", "Elevation of divider's invert"),
        ("max_depth",           '', "Max Depth",       '0',  '',   '',  "Maximum water depth (i.e. distance from invert to ground surface or 0 to use distance from invert to top of highest connecting link)"),
        ("initial_depth",       '', "Initial Depth",   '0',  '',   '',  "Initial water depth in junction"),
        ("surcharge_depth",     '', "Surcharge Depth", '0',  '',   '',  "Depth in excess of maximum depth before flooding occurs"),
        ("ponded_area",         '', "Ponded Area",     '0',  '',   '',  "Area of ponded water when flooded"),
        ("diverted_link",       '', "Diverted Link",   '',   '',   '',  "Name of link which receives the diverted flow"),
        ("flow_divider_type",   '', "Type",            '',   '',   '',  "Type of flow divider"),
        ("cutoff_flow",         '', "Cutoff Flow",     '0',  '',   '',  "Cutoff flow value used for a CUTOFF divider"),
        ("divider_curve",       '', "Tabular Curve Name",   '',   '',   '',  "Name of diversion curve used with a TABULAR divider"),
        ("weir_min_flow",       '', "Weir Min. Flow",       '0',  '',   '',  "Minimum flow at which diversion begins for a WEIR divider"),
        ("weir_max_depth",      '', "Weir Max. Depth",      '0',  '',   '',  "Depth at maximum flow for a WEIR divider"),
        ("weir_coefficient",    '', "Weir Coefficient",     '0',  '',   '',  "Discharge coefficient for a WEIR divider")))

    def __init__(self):
        Junction.__init__(self)

        self.diverted_link = None
        """Name of link which receives the diverted flow."""

        self.flow_divider_type = FlowDividerType.CUTOFF
        """Type of flow divider from FlowDividerType(Enum)"""

        self.max_depth = 0.0
        """Maximum depth of node (i.e., from ground surface to invert)
            (feet or meters). If zero, then the distance from the invert to
            the top of the highest connecting link will be used. """

        self.initial_depth = 0.0
        """Depth of water at the node at the start of the simulation
            (feet or meters)."""

        self.surcharge_depth = 0.0
        """Additional depth of water beyond the maximum depth that is
            allowed before the node floods (feet or meters).
            This parameter can be used to simulate bolted manhole covers
            or force main connections. """

        self.ponded_area = 0.0
        """Area occupied by ponded water atop the node after flooding
            occurs (sq. feet or sq. meters). If the Allow Ponding simulation
            option is turned on, a non-zero value of this parameter will allow
            ponded water to be stored and subsequently returned to the
            conveyance system when capacity exists."""

        self.cutoff_flow = 0
        """Cutoff flow value used for a CUTOFF divider (flow units)."""

        self.divider_curve = None
        """Diversion Curve used with a TABULAR divider"""

        self.weir_min_flow = 0.0
        """Minimum flow at which diversion begins for a WEIR divider"""

        self.weir_max_depth = 0.0
        """Depth at maximum flow for a WEIR divider"""

        self.weir_coefficient = 0.0
        """Discharge coefficient for a WEIR divider"""


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
    field_format = "{:16}\t{:8}\t{:10}\t{:10}\t{:10}\t{:20}\t{:8}\t{:8}\t{:8}\t{:8}\t{:8}\t{}"

    #    attribute, input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",                '', "Name",            '',   '',   '',  "User-assigned name of storage unit"),
        ('',                    '', "X-Coordinate",    '',   '',   '',  "X coordinate of storage unit on study area map"),
        ('',                    '', "Y-Coordinate",    '',   '',   '',  "Y coordinate of storage unit on study area map"),
        ('',                    '', "Description",     '',   '',   '',  "Optional comment or description"),
        ('',                    '', "Tag",             '',   '',   '',  "Optional category or classification"),
        ('',                    '', "Inflows",         'NO', '',   '',  "Click to specify any external inflows received at the storage unit"),
        ('.treatment(node_id)', '', "Treatment",       'NO', '',   '',  "Click to specify any pollutant removal supplied at the storage unit"),
        ("elevation",           '', "Invert El.",      '0',  "ft", "m", "Elevation at the bottom of the storage unit"),
        ("max_depth",           '', "Max Depth",       '0',  '',   '',  "Maximum depth of the storage unit"),
        ("initial_depth",       '', "Initial Depth",   '0',  '',   '',  "Initial depth of water in the storage unit"),
        ("evaporation_factor",  '', "Evap. Factor",    '',   '',   '',  "Fraction of evaporation rate realized"),
        ("seepage_loss",        '', "Seepage Loss",    '',   '',   '',  "Click to specify soil properties that determine seepage loss through the bottom and sloped sides of the storage unit"),
        ("storage_curve_type",  '', "Storage Curve",   '0',  '',   '',  "Method of describing the geometric shape of the storage unit"),
        ("coefficient",         '', "Functional Curve Coefficient",   '',   '',   '',  "A-value in expression Area = A*Depth^B + C"),
        ("exponent",            '', "Functional Curve Exponent",      '0',  '',   '',  "B-value in expression Area = A*Depth^B + C"),
        ("constant",            '', "Functional Curve Constant",      '0',  '',   '',  "C-value in expression Area = A*Depth^B + C"),
        ("storage_curve",       '', "Tabular Curve Name",             '0',  '',   '',  "Name of storage curve to use")))

    def __init__(self):
        Junction.__init__(self)
        self.max_depth = ''
        """Maximum depth of node (i.e., from ground surface to invert)
            (feet or meters). If zero, then the distance from the invert to
            the top of the highest connecting link will be used. """

        self.initial_depth = ''
        """Depth of water at the node at the start of the simulation
            (feet or meters)."""

        self.storage_curve_type = StorageCurveType.TABULAR
        """StorageCurveType: FUNCTIONAL or TABULAR"""

        self.storage_curve = ''
        """Storage Curve containing the relationship between
            surface area and storage depth"""

        self.coefficient = ''
        """A-value in the functional relationship
            between surface area and storage depth."""

        self.exponent = ''
        """B-value in the functional relationship
            between surface area and storage depth."""

        self.constant = ''
        """C-value in the functional relationship
            between surface area and storage depth."""

        self.ponded_area = ''
        """Area occupied by ponded water atop the node after flooding
            occurs (sq. feet or sq. meters). If the Allow Ponding simulation
            option is turned on, a non-zero value of this parameter will allow
            ponded water to be stored and subsequently returned to the
            conveyance system when capacity exists."""

        self.evaporation_factor = ''
        """The fraction of the potential evaporation from the storage units
            water surface that is actually realized."""

        self.seepage_loss = ''
        """The following Green-Ampt infiltration parameters are only used when the storage
            node is intended to act as an infiltration basin:"""

        self.seepage_suction_head = ''
        """Soil capillary suction head (in or mm)."""

        self.seepage_hydraulic_conductivity = ''
        """Soil saturated hydraulic conductivity (in/hr or mm/hr)."""

        self.seepage_initial_moisture_deficit = ''
        """Initial soil moisture deficit (volume of voids / total volume)."""


class DirectInflowType(Enum):
    CONCEN = 1
    MASS = 2


class DirectInflow(Section):
    """Defines characteristics of inflows added directly into a node"""

    field_format = "{:16}\t{:16}\t{:16}\t{:8}\t{:8}\t{:8}\t{:8}\t{:8}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)  # set_text will call __init__ without new_text to do the initialization below
        else:
            Section.__init__(self)

            self.node = ''
            """str: name of node where external inflow enters."""

            self.timeseries = ''
            """str: Name of the time series describing how flow or constituent loading to this node varies with time."""

            self.constituent = ''
            """str: Name of constituent (pollutant) or FLOW"""

            self.format = DirectInflowType.CONCEN
            """DirectInflowType: Type of data contained in constituent_timeseries, concentration or mass flow rate"""

            self.conversion_factor = '1.0'
            """float: Numerical factor used to convert the units of pollutant mass flow rate in constituent_timeseries
            into project mass units per second as specified in [POLLUTANTS]"""

            self.scale_factor = '1.0'
            """float: Scaling factor that multiplies the recorded time series values."""

            self.baseline = '0.0'
            """float: Constant baseline added to the time series values."""

            self.baseline_pattern = ''
            """str: ID of Time Pattern whose factors adjust the baseline inflow on an hourly, daily, or monthly basis"""

    def get_text(self):
        inp = ''
        if self.comment:
            inp = self.comment + '\n'
        if self.constituent.upper() == "FLOW":
            inp_format = "FLOW"
        else:
            inp_format = self.format.name
        inp += self.field_format.format(self.node,
                                        self.constituent,
                                        self.timeseries,
                                        inp_format,
                                        self.conversion_factor,
                                        self.scale_factor,
                                        self.baseline,
                                        self.baseline_pattern)
        return inp

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 0:
            self.node = fields[0]
        if len(fields) > 1:
            self.constituent = fields[1]
        if len(fields) > 2:
            self.timeseries = fields[2]
        if len(fields) > 3 and self.constituent.upper() != "FLOW":
            self.setattr_keep_type("format", DirectInflowType[fields[3]])
        if len(fields) > 4:
            self.conversion_factor = fields[4]
        if len(fields) > 5:
            self.scale_factor = fields[5]
        if len(fields) > 6:
            self.baseline = fields[6]
        if len(fields) > 7:
            self.baseline_pattern = fields[7]


class DryWeatherInflow(Section):
    """Specifies dry weather flow and its quality entering the drainage system at a specific node"""

    field_format = "{:16}\t{:16}\t{:10}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)  # set_text will call __init__ without new_text to do the initialization below
        else:
            Section.__init__(self)

            self.node = ''
            """str: name of node where external inflow enters."""

            self.constituent = ''
            """str: Name of constituent (pollutant) or FLOW"""

            self.average = ''
            """str: Average (or baseline) value of the dry weather inflow of the constituent in the relevant units"""

            self.time_patterns = []
            """str: ID of time pattern used to allow the dry weather flow to vary in a periodic fashion"""

    def get_text(self):
        inp = ''
        if self.comment:
            inp = self.comment + '\n'
        inp += self.field_format.format(self.node,
                                        self.constituent,
                                        self.average) + '\t' + '\t'.join(self.time_patterns)
        return inp

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 2:
            self.node = fields[0]
            self.constituent = fields[1]
            self.average = fields[2]
            if len(fields) > 3:
                self.time_patterns = fields[3:]


class RDIInflow(Section):
    """Defines characteristics of Rainfall-Dependent Infiltration/Inflows entering the system at a node"""

    field_format = "{:16}\t{:16}\t{:10}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)  # set_text will call __init__ without new_text to do the initialization below
        else:
            Section.__init__(self)

            self.node = ''
            """str: name of node where external inflow enters."""

            self.hydrograph_group = ""
            """str: name of an RDII unit hydrograph group specified in the [HYDROGRAPHS] section"""

            self.sewershed_area = ''
            """float: area of the sewershed which contributes RDII to the node (acres or hectares)"""

    def get_text(self):
        inp = ''
        if self.comment:
            inp = self.comment + '\n'
        inp += self.field_format.format(self.node,
                                        self.hydrograph_group,
                                        self.sewershed_area)
        return inp

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 2:
            self.node = fields[0]
            self.hydrograph_group = fields[1]
            self.sewershed_area = fields[2]


class Treatment(Section):
    """Define the treatment properties of a node using a treatment expression"""

    field_format = "{:16}\t{:16}\t{}"

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

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)  # set_text will call __init__ without new_text to do the initialization below
        else:
            Section.__init__(self)

            self.node = ''
            """str: name of node where external inflow enters."""

            self.pollutant = ''
            """Name of pollutant receiving treatment"""

            self.function = ''
            """str: mathematical function expressing treatment result in terms of pollutant concentrations,
            pollutant removals, and other standard variables. Starts with C for concentration or R for removal."""

    def get_text(self):
        inp = ''
        if self.comment:
            inp = self.comment + '\n'
        inp += self.field_format.format(self.node,
                                        self.pollutant,
                                        self.function)
        return inp

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 2:
            self.node = fields[0]
            self.pollutant = fields[1]
            self.function = ' '.join(fields[2:])
