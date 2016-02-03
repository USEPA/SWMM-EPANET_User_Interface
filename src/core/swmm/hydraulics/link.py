from enum import Enum


class Link(object):
    """A link in a SWMM model"""
    def __init__(self, name, inlet_node, outlet_node):
        self.name = name
        """Link Name"""

        self.description = None
        """Optional description of the Link"""

        self.tag = None
        """Optional label used to categorize or classify the Link"""

        self.inlet_node = inlet_node
        """Node on the inlet end of the Link"""

        self.outlet_node = outlet_node
        """Node on the outlet end of the Link"""

        self.vertices = {}
        """Collection of intermediate vertices along the length of the link"""


class Conduit(Link):
    """A conduit in a SWMM model"""
    def __init__(self, name, inlet_node, outlet_node):
        Link.__init__(self, name, inlet_node, outlet_node)
        self.length = 0.0
        """Conduit length (feet or meters)."""

        self.roughness = 0.0
        """Manning's roughness coefficient."""

        self.inlet_offset = 0.0
        """Depth or elevation of the conduit invert above the node invert
            at the upstream end of the conduit (feet or meters)."""

        self.outlet_offset = 0.0
        """Depth or elevation of the conduit invert above the node invert
            at the downstream end of the conduit (feet or meters)."""

        self.initial_flow = 0.0
        """Initial flow in the conduit (flow units)."""

        self.maximum_flow = 0.0
        """Maximum flow allowed in the conduit (flow units)."""

        self.cross_section = None
        """See class CrossSection"""

        self.entry_loss_coefficient = 0.0
        """Head loss coefficient associated with energy losses at the entrance of the conduit"""

        self.exit_loss_coefficient = 0.0
        """Head loss coefficient associated with energy losses at the exit of the conduit"""

        self.loss_coefficient = 0.0
        """Head loss coefficient associated with energy losses along the length of the conduit"""

        self.flap_gate = False
        """True if a flap gate exists that prevents backflow."""


class Pump(Link):
    """A pump link in a SWMM model"""
    def __init__(self, name, inlet_node, outlet_node):
        Link.__init__(self, name, inlet_node, outlet_node)
        self.pump_curve = Curve
        """Associated pump curve"""

        self.initial_status = 0.0
        """Initial status of the pump"""

        self.startup_depth = 0.0
        """Depth at inlet node when the pump turns on"""

        self.shutoff_depth = 0.0
        """Depth at inlet node when the pump turns off"""


class OrificeType(Enum):
    SIDE = 1
    BOTTOM = 2


class Orifice(Link):
    """An orifice link in a SWMM model"""
    def __init__(self, name, inlet_node, outlet_node):
        Link.__init__(self, name, inlet_node, outlet_node)
        self.type = OrificeType.SIDE
        """Type of orifice"""

        self.cross_section = None
        """See class CrossSection"""

        self.inlet_offset = 0.0
        """Depth of bottom of orifice opening from inlet node invert"""

        self.discharge_coefficient = 0.0
        """Discharge coefficient"""

        self.flap_gate = False
        """True if a flap gate exists that prevents backflow."""

        self.o_rate = 0.0
        """Time to open/close a gated orifice"""


class WeirType(Enum):
    TRANSVERSE = 1
    SIDEFLOW = 2
    V_NOTCH = 3
    TRAPEZOIDAL = 4
    ROADWAY = 5


class RoadSurfaceType(Enum):
    PAVED = 1
    GRAVEL = 2


class Weir(Link):
    """A weir link in a SWMM model"""
    def __init__(self, name, inlet_node, outlet_node):
        Link.__init__(self, name, inlet_node, outlet_node)
        self.type = WeirType.TRANSVERSE
        """Type of weir"""

        self.cross_section = None
        """See class CrossSection"""

        self.inlet_offset = 0.0
        """Depth of bottom of weir opening from inlet node invert"""

        self.discharge_coefficient = 0.0
        """Discharge coefficient for central portion of weir"""

        self.flap_gate = False
        """True if weir contains a flap gate to prevent backflow"""

        self.end_contractions = 0.0
        """Number of end contractions"""

        self.end_coefficient = 0
        """Discharge coefficient for flow through the triangular ends of a trapezoidal weir"""

        self.can_surcharge = false
        """True if weir can surcharge"""

        self.road_width = 0.0
        """Width of road lanes and shoulders"""

        self.road_surface = RoadSurfaceType.PAVED
        """Type of road surface"""


class OutletCurveType(Enum):
    TABULAR_DEPTH = 1
    TABULAR_HEAD = 2
    FUNCTIONAL_DEPTH = 3
    FUNCTIONAL_HEAD = 4


class Outlet(Link):
    """An outlet link in a SWMM model"""
    def __init__(self, name, inlet_node, outlet_node):
        Link.__init__(self, name, inlet_node, outlet_node)
        self.inlet_offset = 0.0
        """Depth of outlet above inlet node invert"""

        self.flap_gate = False
        """True if outlet contains a flap gate to prevent backflow"""

        self.coefficient = 0.0
        """Coefficient in outflow expression"""

        self.exponent = 0.0
        """Exponent in outflow expression"""

        self.curve_type = OutletCurveType.TABULAR_DEPTH
        """Method of defining flow as a function of either freeboard depth or head across the outlet"""

        self.rating_curve = Curve
        """Name of rating curve that relates outflow to either depth or head"""


class CrossSectionShape(Enum):
    NotSet = 0
    Circular = 1                  # Full Height
    CircularForceMain = 2         # Full Height, Roughness
    FilledCircular = 3            # Full Height, Filled Depth
    RectangularClosed = 4         # Full Height, Width
    RectangularOpen = 5           # Full Height, Width
    Trapezoidal = 6               # Full Height, Base Width, Side Slopes
    Triangular = 7                # Full Height, Top Width
    HorizontalEllipse = 8         # Full Height, Max. Width
    VerticalEllipse = 9           # Full Height, Max. Width
    Arch = 10                     # Full Height, Max. Width
    Parabolic = 11                # Full Height, Top Width
    Power = 12                    # Full Height, Top Width, Exponent
    RectangularTriangular = 13    # Full Height, Top Width, Triangle Height
    RectangularRound = 14         # Full Height, Top Width, Bottom Radius
    ModifiedBaskethandle = 15     # Full Height, Bottom Width, Top Radius
    Egg = 16                      # Full Height
    Horseshoe = 17                # Full Height Gothic Full Height
    Catenary = 18                 # Full Height
    SemiElliptical = 19           # Full Height
    Baskethandle = 20             # Full Height
    SemiCircular = 21             # Full Height
    IrregularNaturalChannel = 22  # TransectCoordinates
    CustomClosedShape = 23        # Full Height, ShapeCurveCoordinates


class CrossSection:
    """A cross section of a Conduit, Orifice, or Weir

    Attributes:
        shape (CrossSectionShape): Description of `shape`.
    """
    def __init__(self, shape):
        self.shape = shape  # class CrossSectionShape
        """cross-section shape"""

        self.geometry1 = 0.0
        """full height of the cross-section (ft or m)"""

        self.geometry2 = 0.0
        """auxiliary parameters (width, side slopes, etc.)"""

        self.geometry3 = 0.0
        """auxiliary parameters (width, side slopes, etc.)"""

        self.geometry4 = 0.0
        """auxiliary parameters (width, side slopes, etc.)"""

        self.barrels = 0.0
        """number of barrels (i.e., number of parallel pipes of equal size, slope, and
        roughness) associated with a conduit (default is 1)."""

        self.culvert_code = None
        """code number for the conduits inlet geometry if it is a culvert subject to possible inlet flow control"""

        self.curve = Curve(None)
        """associated Shape Curve that defines how width varies with depth."""

        self.transect = Transect(None)
        """ cross-section geometry of an irregular channel"""


class Transect:
    """"""
    def __init__(self, name):
        self.name = name
        """Transect Name"""

        self.description = None
        """Optional description of the Transect"""

        self.station_elevation_data_grid = None
        self.roughness = 0.0
        self.bank_stations = None
        self.stations_modifier = None
        self.elevations_modifier = None
        self.meander_modifier = None
