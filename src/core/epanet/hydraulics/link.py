from enum import Enum

from core.project_base import Section
from core.epanet.curves import Curve
from core.epanet.vertex import Vertex
from core.epanet.patterns import Pattern
from core.metadata import Metadata
from core.coordinate import Link


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


class EpanetLink(Section, Link):
    """A link in an EPANET model"""

    def __init__(self):
        Section.__init__(self)
        Link.__init__(self)

        ## Flag indicating whether an output report is desired for this link
        self.report_flag = ''

        # TODO: sync this with STATUS section:
        ## initial status of a pipe, pump, or valve; can be a speed setting for a pump
        self.initial_status = ''


class Pipe(EpanetLink):
    """A Pipe link in an EPANET model"""

    #    attribute,           input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",                      '', "Pipe ID",            "",    '', '', "User-assigned name of the pipe"),
        ("inlet_node",                '', "Start Node",         "",    '', '', "Node on the inlet end of the pipe"),
        ("outlet_node",               '', "End Node",           "",    '', '', "Node on the outlet end of the pipe"),
        ("description",               '', "Description",        "",    '', '', "Optional description of the pipe"),
        ("tag",                       '', "Tag",                "",    '', '', "Optional label used to categorize or classify the pipe"),
        ("length",                    '', "Length",             "0.0", '(ft)', '(m)',  "Pipe length"),
        ("diameter",                  '', "Diameter",           "0.0", '(in)', '(mm)', "Pipe diameter"),
        ("roughness",                 '', "Roughness",          "0.0", '', '', "Manning's roughness coefficient"),
        ("loss_coefficient",          '', "Loss Coeff.",        "0.0", '', '', "Minor loss coefficient"),
        ("initial_status",            '', "Initial Status",     "",    '', '', "Initial status of a pipe"),
        ("bulk_reaction_coefficient", '', "Bulk Coeff.",        "0.0", '', '', "Bulk reaction coefficient for this pipe"),
        ("wall_reaction_coefficient", '', "Wall Coeff.",        "0.0", '', '', "Wall reaction coefficient for this pipe"),
    ))

    def __init__(self):
        EpanetLink.__init__(self)

        ## pipe length
        self.length = "0.0"

        ## pipe diameter
        self.diameter = "0.0"

        ## Manning's roughness coefficient
        self.roughness = "0.0"

        ## Minor loss coefficient
        self.loss_coefficient = "0.0"

        # See REACTIONS section for this parameter; could add convenience function to find it
        ## bulk reaction coefficient for this pipe
        # self.bulk_reaction_coefficient = "0.0"

        # See REACTIONS section for this parameter; could add convenience function to find it
        ## wall reaction coefficient for this pipe
        # self.wall_reaction_coefficient = "0.0"


class Pump(EpanetLink):
    """A Pump link in an EPANET model"""

    #    attribute,  input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",             '', "Pump ID",            "",    '', '', "User-assigned name of the pump"),
        ("inlet_node",       '', "Start Node",         "",    '', '', "Node on the inlet end of the pump"),
        ("outlet_node",      '', "End Node",           "",    '', '', "Node on the outlet end of the pump"),
        ("description",      '', "Description",        "",    '', '', "Optional description of the pump"),
        ("tag",              '', "Tag",                "",    '', '', "Optional label used to categorize or classify the pump"),
        ("head_curve_name",  '', "Pump Curve",         "",    '', '', "Curve that describes head versus flow for the pump"),
        ("power",            '', "Power",              "0.0", '', '', "Power value for constant energy pump, hp (kW)"),
        ("speed",            '', "Speed",              "0.0", '', '', "Relative speed setting (normal speed is 1.0, 0 means pump is off)"),
        ("pattern",          '', "Pattern",            "",    '', '', "Time pattern that describes how speed setting varies with time"),
        ("initial_status",   '', "Initial Status",     "",    '', '', "Initial status of a pump"),
        ("efficiency_curve_name", '', "Effic. Curve",       "",    '', '', "Efficiency curve name"),
        ("energy_price", '', "Energy Price",       "0.0", '', '', "Energy price for this pump"),
        ("price_pattern", '', "Price Pattern",      "",    '', '', "ID of price pattern for this pump"),
    ))

    def __init__(self):
        EpanetLink.__init__(self)

        # Either power or head_curve_name must be supplied for each pump. The other fields are optional.

        ## power value for constant energy pump, hp (kW)
        self.power = "0.0"

        ## curve that describes head versus flow for the pump
        self.head_curve_name = ''

        ## relative speed setting (normal speed is 1.0, 0 means pump is off)
        self.speed = "0.0"

        ## time pattern that describes how speed setting varies with time
        self.pattern = ''

        # pump energy parameters are in options/energy


class Valve(EpanetLink):
    """A valve link in an EPANET model"""

#    attribute,         input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",                   '', "Valve ID",           "",    '', '', "User-assigned name of the valve"),
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
        EpanetLink.__init__(self)

        ## valve diameter
        self.diameter = "0.0"

        ##  PRV (pressure reducing valve) Pressure, psi (m);
        ##  PSV (pressure sustaining valve) Pressure, psi (m);
        ##  PBV (pressure breaker valve) Pressure, psi (m);
        ##  FCV (flow control valve) Flow (flow units);
        ##  TCV (throttle control valve) Loss Coefficient;
        ##  GPV (general purpose valve) ID of head loss curve
        self.type = ValveType.PRV

        ## Pressure for PRV, PSV, and PBV; flow for FCV, Loss Coefficient for TCV, head loss curve name for GPV
        self.setting = "0.0"

        ## TCV (throttle control valve) Loss Coefficient
        self.minor_loss_coefficient = "0.0"

        ## valve is open or closed
        # TODO: access this: self.fixed_status = FixedStatus.OPEN


class Status(Section):
    """
        Initial status of a link at the start of the simulation.
        Pipes can have a status of OPEN, CLOSED, or CV.
        Pumps can have a status of OPEN, CLOSED, or a speed.
    """

    def __init__(self):
        Section.__init__(self)

        ## Identifier of link whose initial status is being specified
        self.name = ''

        ## Initial status of link
        self.status = ''


