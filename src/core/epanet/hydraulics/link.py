from enum import Enum

from core.project_base import Section
from core.epanet.curves import Curve
from core.epanet.vertex import Vertex
from core.epanet.patterns import Pattern
from core.metadata import Metadata


class PumpType(Enum):
    """Pump Type"""
    POWER = 1
    HEAD = 2


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

        # TODO: sync this with STATUS section:
        self.initial_status = ''
        """initial status of a pipe, pump, or valve; can be a speed setting for a pump"""

class Pipe(Link):
    """A Pipe link in an EPANET model"""


#    attribute,         input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("id",                        '', "Pipe ID",            "",    '', '', "User-assigned name of the pipe"),
        ("inlet_node",                '', "Start Node",         "",    '', '', "Node on the inlet end of the pipe"),
        ("outlet_node",               '', "End Node",           "",    '', '', "Node on the outlet end of the pipe"),
        ("description",               '', "Description",        "",    '', '', "Optional description of the pipe"),
        ("tag",                       '', "Tag",                "",    '', '', "Optional label used to categorize or classify the pipe"),
        ("length",                    '', "Length",             "0.0", '', '', "Pipe length"),
        ("diameter",                  '', "Diameter",           "0.0", '', '', "Pipe diameter"),
        ("roughness",                 '', "Roughness",          "0.0", '', '', "Manning's roughness coefficient"),
        ("loss_coefficient",          '', "Loss Coeff.",        "0.0", '', '', "Minor loss coefficient"),
        ("initial_status",            '', "Initial Status",     "",    '', '', "Initial status of a pipe"),
        ("bulk_reaction_coefficient", '', "Bulk Coeff.",        "0.0", '', '', "Bulk reaction coefficient for this pipe"),
        ("wall_reaction_coefficient", '', "Wall Coeff.",        "0.0", '', '', "Wall reaction coefficient for this pipe"),
    ))

    def __init__(self):
        Link.__init__(self)

        self.length = "0.0"
        """pipe length"""

        self.diameter = "0.0"
        """pipe diameter"""

        self.roughness = "0.0"
        """Manning's roughness coefficient"""

        self.loss_coefficient = "0.0"
        """Minor loss coefficient"""

        # See REACTIONS section for this parameter; could add convenience function to find it
        # self.bulk_reaction_coefficient = "0.0"
        """bulk reaction coefficient for this pipe"""

        # See REACTIONS section for this parameter; could add convenience function to find it
        # self.wall_reaction_coefficient = "0.0"
        """wall reaction coefficient for this pipe"""

class Pump(Link):
    """A Pump link in an EPANET model"""


#    attribute,         input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("id",               '', "Pump ID",            "",    '', '', "User-assigned name of the pump"),
        ("inlet_node",       '', "Start Node",         "",    '', '', "Node on the inlet end of the pump"),
        ("outlet_node",      '', "End Node",           "",    '', '', "Node on the outlet end of the pump"),
        ("description",      '', "Description",        "",    '', '', "Optional description of the pump"),
        ("tag",              '', "Tag",                "",    '', '', "Optional label used to categorize or classify the pump"),
        ("head_curve_name",  '', "Pump Curve",         "",    '', '', "Curve that describes head versus flow for the pump"),
        ("power",            '', "Power",              "0.0", '', '', "Power value for constant energy pump, hp (kW)"),
        ("speed",            '', "Speed",              "0.0", '', '', "Relative speed setting (normal speed is 1.0, 0 means pump is off)"),
        ("pattern",          '', "Pattern",            "",    '', '', "Time pattern that describes how speed setting varies with time"),
        ("initial_status",   '', "Initial Status",     "",    '', '', "Initial status of a pump"),
        ("PumpEnergy.value", '', "Effic. Curve",       "",    '', '', "Efficiency curve name"),
        ("PumpEnergy.value", '', "Energy Price",       "0.0", '', '', "Energy price for this pump"),
        ("PumpEnergy.value", '', "Price Pattern",      "",    '', '', "ID of price pattern for this pump"),
    ))

    def __init__(self):
        Link.__init__(self)

        self.type = PumpType.POWER
        """Either POWER or HEAD must be supplied for each pump. The other keywords are optional."""

        self.power = "0.0"
        """power value for constant energy pump, hp (kW)"""

        self.head_curve_name = ''
        """curve that describes head versus flow for the pump"""

        self.speed = "0.0"
        """relative speed setting (normal speed is 1.0, 0 means pump is off)"""

        self.pattern = ''
        """time pattern that describes how speed setting varies with time"""

        # TODO: access pump-specific energy parameters in options/energy

class Valve(Link):
    """A valve link in an EPANET model"""


#    attribute,         input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("id",                     '', "Valve ID",           "",    '', '', "User-assigned name of the valve"),
        ("inlet_node",             '', "Start Node",         "",    '', '', "Node on the inlet end of the valve"),
        ("outlet_node",            '', "End Node",           "",    '', '', "Node on the outlet end of the valve"),
        ("description",            '', "Description",        "",    '', '', "Optional description of the valve"),
        ("tag",                    '', "Tag",                "",    '', '', "Optional label used to categorize or classify the valve"),
        ("diameter",               '', "Diameter",           "0.0", '', '', "Valve diameter"),
        ("type",                   '', "Type",               "",    '', '', "Valve type"),
        ("setting",                '', "Setting",            "",    '', '', "Pressure for PRV, PSV, and PBV; flow for FCV, Loss Coefficient for TCV, head loss curve name for GPV"),
        ("minor_loss_coefficient", '', "Loss Coeff.",        "",    '', '', "TCV (throttle control valve) Loss Coefficient"),
        ("status",                 '', "Fixed Status",       "",    '', '', "Initial status of a valve"),
    ))

    def __init__(self):
        Link.__init__(self)

        self.diameter = "0.0"
        """valve diameter"""

        self.type = ValveType.PRV
        """ PRV (pressure reducing valve) Pressure, psi (m)
            PSV (pressure sustaining valve) Pressure, psi (m)
            PBV (pressure breaker valve) Pressure, psi (m)
            FCV (flow control valve) Flow (flow units)
            TCV (throttle control valve) Loss Coefficient
            GPV (general purpose valve) ID of head loss curve"""

        self.setting = "0.0"
        """Pressure for PRV, PSV, and PBV; flow for FCV, Loss Coefficient for TCV, head loss curve name for GPV"""

        self.minor_loss_coefficient = "0.0"
        """TCV (throttle control valve) Loss Coefficient"""

        # TODO: access this: self.fixed_status = FixedStatus.OPEN
        """valve is open or closed"""

class Status(Section):
    """
        Initial status of a link at the start of the simulation.
        Pipes can have a status of OPEN, CLOSED, or CV.
        Pumps can have a status of OPEN, CLOSED, or a speed.
    """


    def __init__(self):
        Section.__init__(self)

        self.id = ''
        """Identifier of link whose initial status is being specified"""

        self.status = ''
        """Initial status of link"""

