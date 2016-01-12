from enum import Enum


class Link(object):
    """A link in a SWMM or EPANET model"""
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


class Conduit(Link):
    """A link in a SWMM or EPANET model"""
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

        self.flap_gate = False
        """True if a flap gate exists that prevents backflow."""


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
        self.geometry1 = 0.0
        self.geometry2 = 0.0
        self.geometry3 = 0.0
        self.geometry4 = 0.0
        self.barrels = 0.0
        self.culvert_code = None
        self.curve = Curve(None)
        self.transect = Transect(None)


class Curve:
    """A functional relationship between two quantities.
        Uses: Storage, Shape, Diversion, Tidal, Pump, Rating and Control."""
    def __init__(self, name):
        self.name = name
        """Name of the curve"""

        self.mapping = {}
        """Dictionary mapping input values to output values"""


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
