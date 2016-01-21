from enum import Enum
from core.coordinates import Coordinates
from core.epanet.patterns import Pattern
from core.epanet.curves import Curve


class SourceType(Enum):
    """Water Quality Source Type"""
    CONCENTRATION = 1
    MASS = 2
    FLOW_PACED = 3
    SET_POINT = 4


class MixingModel(Enum):
    """Mixing Model"""
    MIXED = 1
    TWO_COMP = 2
    FIFO = 3
    LIFO = 4


class Node(Coordinates):
    """A node in an EPANET model"""
    def __init__(self, x, y):
        Coordinates.__init__(self, x, y)

        self.name = "Unnamed"
        """Node Name"""

        self.description = ""
        """Optional description of the Node"""

        self.tag = ""
        """Optional label used to categorize or classify the Node"""

        self.initial_quality = 0.0
        """Quality represents concentration for chemicals, hours for water age, or percent for source tracing"""

        self.source_quality = Source
        """defines characteristics of water quality source"""

        self.report_flag = ""
        """Indicates whether reporting is desired at this node"""


class Junction:
    """Junction properties"""
    def __init__(self):
        self.node_id = -1
        """elevation of junction"""

        self.elevation = 0.0
        """elevation of junction"""

        self.demand = "" # Does this need to be a list or just one?
        """characteristics of all demands at this node"""

        self.pattern = ""
        """TODO: decide whether pattern belongs here and document it"""

        self.emitter_coefficient = 0.0
        """Emitters are used to model flow through sprinkler heads or pipe leaks. Flow out of the emitter equals
            the product of the flow coefficient and the junction pressure raised to power  """

    def to_inp(self):
        """format contents of this item for writing to file"""
        return '\t'.join((str(self.node_id), str(self.elevation), str(self.demand), str(self.pattern)))
        # TODO: What is the rule for creating columns? Will any amount of whitespace work?

    def set_from_text(self, text):
        (self.node_id, self.elevation, self.demand, self.pattern) = text.split()


class Reservoir(Node):
    """A Reservoir node"""
    def __init__(self, name, coordinates):
        Node.__init__(self, name, coordinates)

        self.total_head = 0.0
        """Head is the hydraulic head (elevation + pressure head) of water in the reservoir"""

        self.head_pattern = Pattern
        """head pattern can be used to make the reservoir head vary with time"""


class Tank(Node):
    """A Tank node"""
    def __init__(self, name, coordinates):
        Node.__init__(self, name, coordinates)

        self.elevation = 0.0
        """Bottom elevation, ft (m)"""

        self.initial_level = 0.0
        """Initial water level, ft (m)"""

        self.minimum_level = 0.0
        """Minimum water level, ft (m)"""

        self.maximum_level = 0.0
        """Maximum water level, ft (m)"""

        self.diameter = 0.0
        """Nominal diameter, ft (m)"""

        self.minimum_volume = 0.0
        """Minimum volume, cubic ft (cubic meters)"""

        self.volume_curve = Curve
        """If a volume curve is supplied the diameter value can be any non-zero number"""

        self.mixing_model = MixingModel.MIXED
        """Mixing models include:
            Completely Mixed (MIXED)
            Two-Compartment Mixing (2COMP)
            Plug Flow (FIFO)
            Stacked Plug Flow (LIFO)"""

        self.mixing_fraction = 0.0
        """fraction of the total tank volume devoted to the inlet/outlet compartment"""

        self.reaction_coefficient = 0.0
        """used to override the global reaction coefficient"""


class Source:
    """Defines locations of water quality sources"""
    def __init__(self):
        self.Type = SourceType.CONCENTRATION			# CONCENTRATION, MASS, FLOW_PACED, or SET_POINT
        """Source type (CONCENTRATION, MASS, FLOW_PACED, or SET_POINT)"""

        self.Baseline = 0.0			    # real
        """Baseline source strength"""

        self.SourcePattern = Pattern    # (Subclass Pattern)
        """Time pattern ID (optional)"""


class Demand:
    """Define multiple water demands at junction nodes"""
    def __init__(self):
        self.BaseDemand = 0.0	    # real
        """Base demand (flow units)"""

        self.DemandPattern = Pattern    # (Subclass Pattern)
        """Demand pattern ID (optional)"""

        self.Category = ""			# string
        """Name of demand category preceded by a semicolon (optional)"""
