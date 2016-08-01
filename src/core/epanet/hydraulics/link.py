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

    field_format = "{:16}\t{:16}\t{:16}"

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

    def get_text(self):
        """format contents of this item for writing to file"""
        if len(self.id) > 0:
            return self.field_format.format(self.id, self.inlet_node, self.outlet_node)  # self.description
        elif self.comment:
            return self.comment

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split(None, 3)
        if len(fields) > 2:
            (self.id, self.inlet_node, self.outlet_node) = fields[0:3]
            if len(fields) > 3:
                self.description = fields[3]


class Pipe(Link):
    """A Pipe link in an EPANET model"""

    field_format = "{:16}\t{:16}\t{:16}\t{:12}\t{:12}\t{:12}\t{:12}\t{:6}\t{}"

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

            # See REACTIONS section for this parameter; could add convenience function to find it
            # self.bulk_reaction_coefficient = "0.0"
            """bulk reaction coefficient for this pipe"""

            # See REACTIONS section for this parameter; could add convenience function to find it
            # self.wall_reaction_coefficient = "0.0"
            """wall reaction coefficient for this pipe"""

    def get_text(self):
        """format contents of this item for writing to file"""
        if len(self.id) > 0:
            return self.field_format.format(self.id, self.inlet_node, self.outlet_node, self.length, self.diameter,
                                            self.roughness, self.loss_coefficient, self.initial_status, self.comment)
        elif self.comment:
            return self.comment

    def set_text(self, new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        self.__init__()
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
            self.initial_status = fields[7]


class Pump(Link):
    """A Pump link in an EPANET model"""

    field_format = "{:16}\t{:16}\t{:16}"

#    attribute,         input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("id",               '', "Pump ID",            "",    '', '', "User-assigned name of the pump"),
        ("inlet_node",       '', "Start Node",         "",    '', '', "Node on the inlet end of the pump"),
        ("outlet_node",      '', "End Node",           "",    '', '', "Node on the outlet end of the pump"),
        ("description",      '', "Description",        "",    '', '', "Optional description of the pump"),
        ("tag",              '', "Tag",                "",    '', '', "Optional label used to categorize or classify the pump"),
        ("head_curve_id",    '', "Pump Curve",         "",    '', '', "Curve that describes head versus flow for the pump"),
        ("power",            '', "Power",              "0.0", '', '', "Power value for constant energy pump, hp (kW)"),
        ("speed",            '', "Speed",              "0.0", '', '', "Relative speed setting (normal speed is 1.0, 0 means pump is off)"),
        ("pattern",          '', "Pattern",            "",    '', '', "Time pattern that describes how speed setting varies with time"),
        ("initial_status",   '', "Initial Status",     "",    '', '', "Initial status of a pump"),
        ("PumpEnergy.value", '', "Effic. Curve",       "",    '', '', "Efficiency curve ID"),
        ("PumpEnergy.value", '', "Energy Price",       "0.0", '', '', "Energy price for this pump"),
        ("PumpEnergy.value", '', "Price Pattern",      "",    '', '', "ID of price pattern for this pump"),
    ))

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            Link.__init__(self)

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

            # TODO: access pump-specific energy parameters in options/energy

    def get_text(self):
        """format contents of this item for writing to file"""
        if len(self.id) > 0:
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
        elif self.comment:
            return self.comment

    def set_text(self, new_text):
        self.__init__()
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

    field_format = "{:16}\t{:16}\t{:16}\t{:12}\t{:4}\t{:12}\t{:12}\t{}"

#    attribute,         input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("id",                     '', "Valve ID",           "",    '', '', "User-assigned name of the valve"),
        ("inlet_node",             '', "Start Node",         "",    '', '', "Node on the inlet end of the valve"),
        ("outlet_node",            '', "End Node",           "",    '', '', "Node on the outlet end of the valve"),
        ("description",            '', "Description",        "",    '', '', "Optional description of the valve"),
        ("tag",                    '', "Tag",                "",    '', '', "Optional label used to categorize or classify the valve"),
        ("diameter",               '', "Diameter",           "0.0", '', '', "Valve diameter"),
        ("type",                   '', "Type",               "",    '', '', "Valve type"),
        ("setting",                '', "Setting",            "",    '', '', "Pressure for PRV, PSV, and PBV; flow for FCV, Loss Coefficient for TCV, head loss curve ID for GPV"),
        ("minor_loss_coefficient", '', "Loss Coeff.",        "",    '', '', "TCV (throttle control valve) Loss Coefficient"),
        ("status",                 '', "Fixed Status",       "",    '', '', "Initial status of a valve"),
    ))

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
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
            """Pressure for PRV, PSV, and PBV; flow for FCV, Loss Coefficient for TCV, head loss curve ID for GPV"""

            self.minor_loss_coefficient = "0.0"
            """TCV (throttle control valve) Loss Coefficient"""

            # TODO: access this: self.fixed_status = FixedStatus.OPEN
            """valve is open or closed"""

    def get_text(self):
        """format contents of this item for writing to file"""
        if len(self.id) > 0:
            return self.field_format.format(self.id,
                                            self.inlet_node,
                                            self.outlet_node,
                                            self.diameter,
                                            self.type.name,
                                            self.setting,
                                            self.minor_loss_coefficient,
                                            self.comment)
        elif self.comment:
            return self.comment

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 2:
            self.id = fields[0]
            self.inlet_node = fields[1]
            self.outlet_node = fields[2]
            if len(fields) > 3:
                self.diameter = fields[3]
            if len(fields) > 4:
                self.type = ValveType[fields[4].upper()]
            if len(fields) > 5:
                self.setting = fields[5]
            if len(fields) > 6:
                self.minor_loss_coefficient = fields[6]


class Status(Section):
    """
        Initial status of a link at the start of the simulation.
        Pipes can have a status of OPEN, CLOSED, or CV.
        Pumps can have a status of OPEN, CLOSED, or a speed.
    """

    field_format = "{:16}\t{}\t{}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            Section.__init__(self)

            self.id = ''
            """Identifier of link whose initial status is being specified"""

            self.status = ''
            """Initial status of link"""

    def get_text(self):
        """format contents of this item for writing to file"""
        if len(self.id) > 0:
            return self.field_format.format(self.id,
                                            self.status,
                                            self.comment)
        elif self.comment:
            return self.comment

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 1:
            self.id = fields[0]
            self.status = fields[1]
