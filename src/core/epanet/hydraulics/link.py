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

        self.link_id = "Unnamed"
        """Link Name"""

        self.inlet_node = None
        """Node on the inlet end of the Link"""

        self.outlet_node = None
        """Node on the outlet end of the Link"""

        self.description = None
        """Optional description of the Link"""

        self.tag = None
        """Optional label used to categorize or classify the Link"""

        self.vertices = [Vertex]  # Collection of Vertices
        """Coordinates of interior vertex points """

        self.report_flag = ""
        """Flag indicating whether an output report is desired for this link"""

    @property
    def text(self):
        """format contents of this item for writing to file"""
        return str(self.link_id) + "   "\
            + str(self.inlet_node) + "   "\
            + str(self.outlet_node) + "   "\
            + str(self.description)
        # TODO: What is the rule for creating columns? Will any amount of whitespace work?

    @text.setter
    def text(self, new_text):
        comment_split = str.split(new_text, ';', 1)
        if len(comment_split) == 2:
            line = comment_split[0]
            self.comment = ';' + comment_split[1]
        fields = new_text.split(None, 3)
        if len(fields) > 2:
            (self.link_id, self.inlet_node, self.outlet_node) = fields[0:2]
            if len(fields) > 3:
                self.description = fields[3]


class Pipe(Link):
    """A Pipe link in an EPANET model"""
    def __init__(self):
        Link.__init__(self)

        self.length = 0.0
        """pipe length"""

        self.diameter = 0.0
        """pipe diameter"""

        self.roughness = 0.0
        """Manning's roughness coefficient"""

        self.loss_coefficient = 0.0
        """Minor loss coefficient"""

        self.status = InitialStatusPipe.OPEN
        """initial status of a pipe, open, closed, or check valve"""

        self.bulk_reaction_coefficient = 0.0
        """bulk reaction coefficient for this pipe"""

        self.wall_reaction_coefficient = 0.0
        """wall reaction coefficient for this pipe"""

    @property
    def text(self):
        """format contents of this item for writing to file"""
        if len(self.link_id) > 0:
            return str(self.link_id) + '\t'\
                   + str(self.inlet_node) + '\t'\
                   + str(self.outlet_node) + '\t'\
                   + str(self.length) + '\t'\
                   + str(self.diameter) + '\t'\
                   + str(self.roughness) + '\t'\
                   + str(self.loss_coefficient) + '\t'\
                   + str(self.status) \
                   + ('\t' + self.comment if len(self.comment) > 0 else '')
        elif len(self.comment) > 0:
            return self.comment
        # TODO: What is the rule for creating columns? Will any amount of whitespace work?

    @text.setter
    def text(self, new_text):
        """read properties from text"""
        comment_split = str.split(new_text, ';', 1)
        if len(comment_split) == 2:
            new_text = comment_split[0]
            self.comment = ';' + comment_split[1]
        fields = new_text.split(None, 6)
        if len(fields) > 2:
            self.link_id = fields[0]
            self.inlet_node = fields[1]
            self.outlet_node = fields[2]
        if len(fields) > 6:
            self.length = fields[3]
            self.diameter = fields[4]
            self.roughness = fields[5]
            self.loss_coefficient = fields[6]
        if len(fields) > 7:
            self.status = fields[7]


class Pump(Link):
    """A Pump link in an EPANET model"""
    def __init__(self):
        Link.__init__(self)

        self.type = PumpType.POWER
        """Either POWER or HEAD must be supplied for each pump. The other keywords are optional."""

        self.power = 0.0
        """power value for constant energy pump, hp (kW)"""

        self.head_curve_id = ""
        """curve that describes head versus flow for the pump"""

        self.speed = 0.0
        """relative speed setting (normal speed is 1.0, 0 means pump is off)"""

        self.pattern = Pattern()
        """time pattern that describes how speed setting varies with time"""

        self.initial_status = InitialStatusPump.OPEN
        """initial status of a pump, can also include a speed setting"""

        self.energy = PumpEnergy()
        """parameters used to compute pumping energy and cost"""

    @property
    def text(self):
        """format contents of this item for writing to file"""
        return str(self.link_id) + '\t'\
            + str(self.inlet_node) + '\t'\
            + str(self.outlet_node) + '\t'\
            + str(self.head_curve_id)\
            + ('\t' + self.comment if len(self.comment) > 0 else '')
        # TODO: format for remaining fields?
        # TODO: What is the rule for creating columns? Will any amount of whitespace work?

    @text.setter
    def text(self, new_text):
        comment_split = str.split(new_text, ';', 1)
        if len(comment_split) == 2:
            new_text = comment_split[0]
            self.comment = ';' + comment_split[1]
        fields = new_text.split(None, 3)
        self.link_id = fields[0]
        self.inlet_node = fields[1]
        self.outlet_node = fields[2]
        self.head_curve_id = fields[3]
        """TODO: Populate additional fields: self.speed = ... """


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

    @property
    def text(self):
        """format contents of this item for writing to file"""
        return str(self.link_id) + '\t'\
            + str(self.inlet_node) + '\t'\
            + str(self.outlet_node) + '\t'\
            + str(self.diameter) + '\t'\
            + str(self.type) + '\t'\
            + str(self.setting) + '\t'\
            + str(self.loss_coefficient)
        # TODO: What is the rule for creating columns? Will any amount of whitespace work?

    @text.setter
    def text(self, new_text):
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

        self.Value = 0.0		        # real
        """Value of price or efficiency"""

        self.EnergyPattern = Pattern   # (Subclass Pattern)
        """If entered as pattern, this is the associated pattern"""

        self.EnergyCurve = Curve       # (Subclass Curve)
        """If efficiency is entered as a curve, this is the associated curve"""


