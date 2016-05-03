from enum import Enum
from core.coordinates import Coordinates
from core.epanet.patterns import Pattern
from core.epanet.curves import Curve
from core.inputfile import Section


class SourceType(Enum):
    """Water Quality Source Type"""
    CONCEN = 1
    MASS = 2
    FLOWPACED = 3
    SETPOINT = 4


class MixingModel(Enum):
    """Mixing Model"""
    MIXED = 1
    TWO_COMP = 2
    FIFO = 3
    LIFO = 4


# class Node(Coordinates):
#     """A node in an EPANET model"""
#     def __init__(self, x, y):
#         Coordinates.__init__(self, x, y)
#
#         self.name = "Unnamed"
#         """Node Name"""
#
#         self.description = ""
#         """Optional description of the Node"""
#
#         self.tag = ""
#         """Optional label used to categorize or classify the Node"""
#
#         self.initial_quality = 0.0
#         """"""
#
#         self.source_quality = Source()
#         """defines characteristics of water quality source"""
#
#         self.report_flag = ""
#         """Indicates whether reporting is desired at this node"""

class Coordinate(Section):
    field_format = "{:16}\t{:16}\t{:16}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            Section.__init__(self)

            self.node_id = ''
            """Identifier of node at this location"""

            self.x = '0.0'
            """east/west location coordinate"""

            self.y = '0.0'
            """north/south location coordinate"""

    def get_text(self):
        """format contents of this item for writing to file"""
        return self.field_format.format(self.node_id, self.x, self.y)

    def set_text(self, new_text):
        (self.node_id, self.x, self.y) = new_text.split()


class Quality(Section):
    """Initial water quality at a node."""

    field_format = "{:16}\t{}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            Section.__init__(self)

            self.node_id = ''
            """elevation of junction"""

            self.initial_quality = '0.0'
            """concentration for chemicals, hours for water age, or percent for source tracing"""

    def get_text(self):
        """format contents of this item for writing to file"""
        return self.field_format.format(self.node_id, self.initial_quality)

    def set_text(self, new_text):
        (self.node_id, self.initial_quality) = new_text.split()


class Junction(Section):
    """Junction properties"""

    field_format = "{:16}\t{:6}\t{:6}\t{:7}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            Section.__init__(self)
            self.node_id = ''
            """node identifier/name"""

            self.elevation = ''
            """elevation of junction"""

            self.base_demand_flow = ''
            """Base demand flow, characteristic of all demands at this node"""

            self.demand_pattern_id = ''
            """Demand pattern ID, optional"""

            self.emitter_coefficient = ''
            """ Emitters are used to model flow through sprinkler heads or pipe leaks. Flow out of the emitter equals
                the product of the flow coefficient and the junction pressure raised to EMITTER EXPONENT, which
                defaults to 0.5 and can be set in OPTIONS section."""

    def get_text(self):
        """format contents of this item for writing to file"""
        return self.field_format.format(self.node_id, self.elevation, self.base_demand_flow, self.demand_pattern_id)

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 0:
            self.node_id = fields[0]
        if len(fields) > 1:
            self.elevation = fields[1]
        if len(fields) > 2:
            self.base_demand_flow = fields[2]
        if len(fields) > 3:
            self.demand_pattern_id = fields[3]


class Reservoir(Section):
    """A Reservoir node"""

    field_format = "{:16}\t{:6}\t{:6}\t{}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            Section.__init__(self)
            self.node_id = ''
            """node identifier/name"""

            self.total_head = "0.0"
            """Head is the hydraulic head (elevation + pressure head) of water in the reservoir"""

            self.head_pattern_id = ''
            """head pattern can be used to make the reservoir head vary with time"""

    def get_text(self):
        """format contents of this item for writing to file"""
        return self.field_format.format(self.node_id, self.total_head, self.head_pattern_id, self.comment)

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 0:
            self.node_id = fields[0]
        if len(fields) > 1:
            self.total_head = fields[1]
        if len(fields) > 2:
            self.head_pattern_id = fields[2]


class Tank(Section):
    """A Tank node"""

    field_format = " {:16}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:16}\t{}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            Section.__init__(self)
            self.node_id = ''
            """node identifier/name"""

            self.elevation = "0.0"
            """Bottom elevation, ft (m)"""

            self.initial_level = "0.0"
            """Initial water level, ft (m)"""

            self.minimum_level = "0.0"
            """Minimum water level, ft (m)"""

            self.maximum_level = "0.0"
            """Maximum water level, ft (m)"""

            self.diameter = "0.0"
            """Nominal diameter, ft (m)"""

            self.minimum_volume = "0.0"
            """Minimum volume, cubic ft (cubic meters)"""

            self.volume_curve = ''
            """If a volume curve is supplied the diameter value can be any non-zero number"""

            # refer to [REACTIONS] section for reaction coefficient

    def get_text(self):
        """format contents of this item for writing to file"""
        return self.field_format.format(self.node_id, self.elevation, self.initial_level,
                                        self.minimum_level, self.maximum_level, self.diameter,
                                        self.minimum_volume, self.volume_curve, self.comment)

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 0:
            self.node_id = fields[0]
        if len(fields) > 1:
            self.elevation = fields[1]
        if len(fields) > 2:
            self.initial_level = fields[2]
        if len(fields) > 3:
            self.minimum_level = fields[3]
        if len(fields) > 4:
            self.maximum_level = fields[4]
        if len(fields) > 5:
            self.diameter = fields[5]
        if len(fields) > 6:
            self.minimum_volume = fields[6]
        if len(fields) > 7:
            self.volume_curve = fields[7]


class Mixing(Section):
    """Mixing model and volume fraction of a Tank"""

    field_format = "{:16}\t{:12}\t{:12}\t{}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            Section.__init__(self)
            self.node_id = ''
            """node identifier/name"""

            self.mixing_model = MixingModel.MIXED
            """Mixing models include:
                Completely Mixed (MIXED)
                Two-Compartment Mixing (2COMP)
                Plug Flow (FIFO)
                Stacked Plug Flow (LIFO)"""

            self.mixing_fraction = "0.0"
            """fraction of the total tank volume devoted to the inlet/outlet compartment"""

    def get_text(self):
        """format contents of this item for writing to file"""
        return self.field_format.format(self.node_id,
                                        self.mixing_model.name.replace("TWO_", "2"),
                                        self.mixing_fraction,
                                        self.comment)

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 0:
            self.node_id = fields[0]
        if len(fields) > 1:
            self.mixing_model = MixingModel[fields[1].upper().replace("2", "TWO_")]
        if len(fields) > 2:
            self.mixing_fraction = fields[2]


class Source(Section):
    """Defines locations of water quality sources"""

    field_format = "{:16}\t{:14}\t{:12}\t{}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            Section.__init__(self)

            self.node_id = ''

            self.source_type = SourceType.CONCEN # TRATION
            """Source type (CONCEN, MASS, FLOWPACED, or SETPOINT)"""

            self.baseline_strength = '0.0'                  # real, but stored as string
            """Baseline source strength"""

            self.pattern_id = ""                            # string
            """Time pattern ID (optional)"""

    def get_text(self):
        inp = ''
        if self.comment:
            inp = self.comment + '\n'
        inp += self.field_format.format(self.node_id,
                                        self.source_type.name,
                                        self.baseline_strength,
                                        self.pattern_id)
        return inp

    def set_text(self, new_text):
        self.__init__()
        fields = new_text.split()
        if len(fields) > 0:
            self.node_id = fields[0]
        if len(fields) > 1:
            self.source_type = SourceType[fields[1].upper()]
        if len(fields) > 2:
            self.baseline_strength = fields[2]
        if len(fields) > 3:
            self.pattern_id = fields[3]


class Demand(Section):
    """Define multiple water demands at junction nodes"""

    field_format = "{:16}\t{:9}\t{:10}\t{}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            Section.__init__(self)

            self.junction_id = ''
            """Junction this demand applies to"""

            self.base_demand = "0.0"       # real, stored as string
            """Base demand (flow units)"""

            self.demand_pattern = ''     # string
            """Demand pattern ID (optional)"""

            self.category = ''          # string
            """Name of demand category preceded by a semicolon (optional)"""

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
