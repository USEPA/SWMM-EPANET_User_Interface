from enum import Enum

from core.inputfile import Section
from core.epanet.curves import Curve
from core.epanet.vertex import Vertex
from core.epanet.patterns import Pattern


class InitialStatusPipe(Enum):
    """status of a pipe"""
    OPEN = 1
    CLOSED = 2
    CV = 3


class PumpType(Enum):
    """Pump Type"""
    POWER = 1
    HEAD = 2


class PumpEnergyType(Enum):
    """Pump Energy Type"""
    PRICE = 1
    PATTERN = 2
    EFFICIENCY = 3


class InitialStatusPump(Enum):
    """Initial status of a pump"""
    OPEN = 1
    CLOSED = 2


class ValveType(Enum):
    """Valve Type"""
    PRV = 1
    PSV = 2
    PBV = 3
    FCV = 4
    TCV = 5
    GPV = 6


class FixedStatus(Enum):
    """Fixed status of a valve"""
    OPEN = 1
    CLOSED = 2


class Link(Section):
    """A link in an EPANET model"""
    def __init__(self):
        Section.__init__(self)

        self.id = "Unnamed"
        """Link Identifier/Name"""

        self.inlet_node = ''
        """Node on the inlet end of the Link"""

        self.outlet_node = ''
        """Node on the outlet end of the Link"""

        self.description = ''
        """Optional description of the Link"""

        self.tag = ''
        """Optional label used to categorize or classify the Link"""

        self.vertices = []  # list of Vertex
        """Coordinates of interior vertex points """

        self.report_flag = ''
        """Flag indicating whether an output report is desired for this link"""

    def get_text(self):
        """format contents of this item for writing to file"""
        return str(self.link_id) + "   "\
            + str(self.inlet_node) + "   "\
            + str(self.outlet_node) + "   "\
            + str(self.description)
        # TODO: What is the rule for creating columns? Will any amount of whitespace work?

    def set_text(self, new_text):
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split(None, 3)
        if len(fields) > 2:
            (self.link_id, self.inlet_node, self.outlet_node) = fields[0:3]
            if len(fields) > 3:
                self.description = fields[3]


class Pipe(Link):
    """A Pipe link in an EPANET model"""

    field_format = "{:16}\t{:16}\t{:16}\t{:12}\t{:12}\t{:12}\t{:12}\t{:6}\t{}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            Link.__init__(self)

            self.length = "0.0"
            """pipe length"""

            self.diameter = "0.0"
            """pipe diameter"""

            self.roughness = "0.0"
            """Manning's roughness coefficient"""

            self.loss_coefficient = "0.0"
            """Minor loss coefficient"""

            self.status = InitialStatusPipe.OPEN
            """initial status of a pipe, open, closed, or check valve"""

            # See REACTIONS section for these parameters
            # self.bulk_reaction_coefficient = "0.0"
            """bulk reaction coefficient for this pipe"""

            # self.wall_reaction_coefficient = "0.0"
            """wall reaction coefficient for this pipe"""

    def get_text(self):
        """format contents of this item for writing to file"""
        if self.id:
            return self.field_format.format(self.id, self.inlet_node, self.outlet_node, self.length, self.diameter,
                                            self.roughness, self.loss_coefficient, self.status.name, self.comment)
        elif self.comment:
            return self.comment

    def set_text(self, new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split(None, 8)
        if len(fields) > 2:
            self.id, self.inlet_node, self.outlet_node = fields[0:3]
        if len(fields) > 6:
            self.length = fields[3]
            self.diameter = fields[4]
            self.roughness = fields[5]
            self.loss_coefficient = fields[6]
        if len(fields) > 7:
            self.status = InitialStatusPipe[fields[7].upper()]


class Pump(Link):
    """A Pump link in an EPANET model"""

    field_format = "{:16}\t{:16}\t{:16}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            Link.__init__(self)

            self.id = ''
            """Identifier/name of this pipe"""

            self.type = PumpType.POWER
            """Either POWER or HEAD must be supplied for each pump. The other keywords are optional."""

            self.power = "0.0"
            """power value for constant energy pump, hp (kW)"""

            self.head_curve_id = ''
            """curve that describes head versus flow for the pump"""

            self.speed = "0.0"
            """relative speed setting (normal speed is 1.0, 0 means pump is off)"""

            self.pattern = ''
            """time pattern that describes how speed setting varies with time"""

            self.initial_status = InitialStatusPump.OPEN
            """initial status of a pump, can also include a speed setting"""

            self.energy = PumpEnergy()
            """parameters used to compute pumping energy and cost"""

    def get_text(self):
        """format contents of this item for writing to file"""
        txt = self.field_format.format(self.id, self.inlet_node, self.outlet_node)
        if self.type == PumpType.HEAD:
            txt += "\tHEAD " + self.head_curve_id
        else:
            txt += "\tPOWER " + self.power
        if self.pattern:
            txt += "\tPATTERN " + self.pattern
        if self.speed != "0.0":
            txt += "\tSPEED " + self.speed
        if self.comment:
            comment_stripped = self.comment.replace(';', '').strip()
            if comment_stripped:
                txt += "\t; " + comment_stripped
        return txt

    def set_text(self, new_text):
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 2:
            self.id, self.inlet_node, self.outlet_node = fields[0:3]
            for key_index in range(3, len(fields) - 1, 2):
                value_index = key_index + 1
                if fields[key_index].upper() == "HEAD":
                    self.type = PumpType.HEAD
                    self.head_curve_id = fields[value_index]
                elif fields[key_index].upper() == "POWER":
                    self.type = PumpType.POWER
                    self.power = fields[value_index]
                elif fields[key_index].upper() == "PATTERN":
                    self.pattern = fields[value_index]
                elif fields[key_index].upper() == "SPEED":
                    self.speed = fields[value_index]


class Valve(Link):
    """A valve link in an EPANET model"""
    def __init__(self):
        Link.__init__(self)

        self.diameter = 0.0
        """valve diameter"""

        self.type = ValveType.PRV
        """PRV (pressure reducing valve) Pressure, psi (m)
        PSV (pressure sustaining valve) Pressure, psi (m)
        PBV (pressure breaker valve) Pressure, psi (m)
        FCV (flow control valve) Flow (flow units)
        TCV (throttle control valve) Loss Coefficient
        GPV (general purpose valve) ID of head loss curve"""

        self.setting = 0.0
        """Pressure for PRV, PSV, and PBV; flow for FCV"""

        self.loss_coefficient = 0.0
        """TCV (throttle control valve) Loss Coefficient"""

        self.valve_curve = Curve()
        """GPV (general purpose valve) head loss curve"""

        self.fixed_status = FixedStatus.OPEN
        """valve is open or closed"""

    def get_text(self):
        """format contents of this item for writing to file"""
        return str(self.link_id) + '\t'\
            + str(self.inlet_node) + '\t'\
            + str(self.outlet_node) + '\t'\
            + str(self.diameter) + '\t'\
            + str(self.type) + '\t'\
            + str(self.setting) + '\t'\
            + str(self.loss_coefficient)
        # TODO: What is the rule for creating columns? Will any amount of whitespace work?

    def set_text(self, new_text):
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        self.link_id = fields[0]
        self.inlet_node = fields[1]
        self.outlet_node = fields[2]
        self.diameter = fields[3]
        self.type = fields[4]
        self.setting = fields[5]
        self.loss_coefficient = fields[6]


class PumpEnergy:
    """Defines parameters used to compute pumping energy and cost"""
    def __init__(self):
        self.PricePatternEfficiency = PumpEnergyType.PRICE 	# PRICE, PATTERN, or EFFICIENCY
        """Indicator whether this pump energy specification is entered as price, pattern, or efficiency"""

        self.value = 0.0		        # real
        """Value of price or efficiency"""

        self.energy_pattern = ""       # string
        """If entered as pattern, this is the associated pattern ID"""

        self.energy_curve = ""          # string
        """If efficiency is entered as a curve, this is the associated curve ID"""


