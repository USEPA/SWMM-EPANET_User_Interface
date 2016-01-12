from enum import Enum

import core.swmm.groundwater


class Node(object):
    """A node in a SWMM or EPANET model"""
    def __init__(self, name, coordinates):
        self.name = name
        """Node Name"""

        self.description = None
        """Optional description of the Node"""

        self.tag = None
        """Optional label used to categorize or classify the Node"""

        self.coordinates = coordinates
        """Coordinates of Node location (x, y)"""

        self.inflows = {}
        """List of external direct, dry weather, or RDII inflows"""

        self.treatments = {}
        """List of treatment functions for pollutants entering the node"""

        self.invert_elev = None
        """Invert elevation of the Node (feet or meters)"""


class JunctionNode(Node):
    """A Junction node"""
    def __init__(self, name, coordinates):
        Node.__init__(self, name, coordinates)

        self.max_depth = 0.0
        """Maximum depth of junction (i.e., from ground surface to invert)
            (feet or meters). If zero, then the distance from the invert to
            the top of the highest connecting link will be used. """

        self.initial_depth = 0.0
        """Depth of water at the junction at the start of the simulation
            (feet or meters)."""

        self.surcharge_depth = 0.0
        """Additional depth of water beyond the maximum depth that is
            allowed before the junction floods (feet or meters).
            This parameter can be used to simulate bolted manhole covers
            or force main connections. """

        self.ponded_area = 0.0
        """Area occupied by ponded water atop the junction after flooding
            occurs (sq. feet or sq. meters). If the Allow Ponding simulation
            option is turned on, a non-zero value of this parameter will allow
            ponded water to be stored and subsequently returned to the
            conveyance system when capacity exists."""


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


class OutfallNode(Node):
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
    def __init__(self, name, coordinates):
        Node.__init__(self, name, coordinates)

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
    def __init__(self, name, coordinates):
        self.min_flow = 0.0
        """Minimum flow at which diversion begins (flow units)."""

        self.max_depth = 0.0
        """Vertical height of WEIR opening (feet or meters)"""

        self.coefficient = 0.0
        """Product of WEIR's discharge coefficient and its length.
            Weir coefficients are typically in the range of
            2.65 to 3.10 per foot, for flows in CFS."""


class FlowDividerNode(JunctionNode):
    """Flow Dividers are drainage system nodes that divert inflows to
        a specific conduit in a prescribed manner. A flow divider can
        have no more than two conduit links on its discharge side.
        Flow dividers are only active under Kinematic Wave routing
        and are treated as simple junctions under Dynamic Wave routing.
    """
    def __init__(self, name, coordinates, flow_divider_type):
        Node.__init__(self, name, coordinates)

        self.diverted_link = None
        """Name of link which receives the diverted flow."""

        self.flow_divider_type = flow_divider_type
        """Type of flow divider from FlowDividerType(Enum)"""

        self.cutoff_flow = 0
        """Cutoff flow value used for a CUTOFF divider (flow units)."""

        self.tabular_curve = None
        """Diversion Curve used with a TABULAR divider"""

        self.weir = None
        """WeirDivider used with a WEIR divider"""


class StorageCurveType(Enum):
    """Type of flow divider. Choices are:
        CUTOFF (diverts all inflow above a defined cutoff value),
        OVERFLOW (diverts all inflow above the flow capacity of the
                non-diverted link),
        TABULAR (uses a Diversion Curve to express diverted flow as a
                function of the total inflow),
        WEIR (uses a weir equation to compute diverted flow).
    """
    FUNCTIONAL = 1
    TABULAR = 2


class StorageUnit(JunctionNode):
    """Storage Units are drainage system nodes that provide storage volume.
        Physically they could represent storage facilities as small as
        a catch basin or as large as a lake. The volumetric properties
        of a storage unit are described by a function or table of
        surface area versus height.
    """
    def __init__(self, name, coordinates, storage_curve_type):
        Node.__init__(self, name, coordinates)
        self.evaporation_factor = 0.0
        """The fraction of the potential evaporation from the storage unit’s
            water surface that is actually realized."""

        self.infiltration = core.swmm.groundwater.GreenAmptInfiltration()
        """Set of GreenAmpt parameters that describe how water can infiltrate
            into the native soil below the unit. To disable any infiltration,
            set this to None or the parameters inside to zero."""

        self.storage_curve_type = storage_curve_type
        """StorageCurveType: FUNCTIONAL or TABULAR"""

        self.coefficient = 0.0
        """A-value in the functional relationship
            between surface area and storage depth."""

        self.exponent = 0.0
        """B-value in the functional relationship
            between surface area and storage depth."""

        self.constant = 0.0
        """C-value in the functional relationship
            between surface area and storage depth."""

        self.tabular_curve = None
        """Storage Curve containing the relationship between
            surface area and storage depth"""