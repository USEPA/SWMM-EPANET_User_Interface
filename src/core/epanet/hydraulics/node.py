from enum import Enum
from core.coordinates import Coordinates
from core.epanet.patterns import Pattern
from core.epanet.curves import Curve
from core.inputfile import Section

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

        self.source_quality = Source()
        """defines characteristics of water quality source"""

        self.report_flag = ""
        """Indicates whether reporting is desired at this node"""


class Junction:
    """Junction properties"""

    field_format = " {:19}\t{}"

    def __init__(self):
        self.node_id = -1
        """elevation of junction"""

        self.elevation = 0.0
        """elevation of junction"""

        self.demand = ""  # Does this need to be a list or just one?
        """characteristics of all demands at this node"""

        self.pattern = ""
        # TODO: decide whether pattern belongs here and document it"""

        self.emitter_coefficient = 0.0
        """Emitters are used to model flow through sprinkler heads or pipe leaks. Flow out of the emitter equals
            the product of the flow coefficient and the junction pressure raised to power  """

    def get_text(self):
        """format contents of this item for writing to file"""
        return '\t'.join((str(self.node_id), str(self.elevation), str(self.demand), str(self.pattern)))
        # TODO: What is the rule for creating columns? Will any amount of whitespace work?

    def set_text(self, new_text):
        (self.node_id, self.elevation, self.demand, self.pattern) = new_text.split()


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
        self.source_type = SourceType.CONCENTRATION			# CONCENTRATION, MASS, FLOW_PACED, or SET_POINT
        """Source type (CONCENTRATION, MASS, FLOW_PACED, or SET_POINT)"""

        self.baseline = 0.0			    # real
        """Baseline source strength"""

        self.source_pattern = ""        # string
        """Time pattern ID (optional)"""


class Demands(Section):

    SECTION_NAME = "[DEMANDS]"

    DEFAULT_COMMENT = ";ID    \tDemand   \tPattern   \tCategory\n;------\t---------\t----------\t--------"

    def set_text(self, new_text):
        self.value = []
        for line in new_text.splitlines():
            if line.startswith(';') or line.startswith('['):
                self.set_comment_check_section(line)  # Only use this on lines that start with special characters
            else:
                self.value.append(Demand(line))       # Allow trailing comment to be part of a Demand (Category)


class Demand(Section):
    """Define multiple water demands at junction nodes"""

    field_format = "{:7}\t{:9}\t{:10}\t{}"

    def __init__(self, new_text=None):
        Section.__init__(self)

        self.junction_id = ''
        """Junction this demand applies to"""

        self.base_demand = 0.0       # real
        """Base demand (flow units)"""

        self.demand_pattern = ""     # string
        """Demand pattern ID (optional)"""

        self.category = ""          # string
        """Name of demand category preceded by a semicolon (optional)"""

        if new_text:
            self.set_text(new_text)

    def get_text(self):
        inp = ''
        if self.comment:
            inp = self.comment + '\n'
        inp += self.field_format.format(self.junction_id,
                                        self.base_demand,
                                        self.demand_pattern,
                                        self.category)
        return inp

    def set_text(self, new_text):
        self.__init__()
        fields = new_text.split()
        if len(fields) > 0:
            self.junction_id = fields[0]
        if len(fields) > 1:
            self.base_demand = fields[1]
        if len(fields) > 2:
            self.demand_pattern = fields[2]
        if len(fields) > 3:
            self.category = fields[3]
