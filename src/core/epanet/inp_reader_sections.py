import traceback
from enum import Enum
from core.project_base import Section
from core.metadata import Metadata
from core.epanet.curves import CurveType
from core.epanet.curves import Curve
from core.epanet.labels import MeterType
from core.epanet.labels import Label
from core.epanet.patterns import Pattern
from core.epanet.title import Title
from core.epanet.hydraulics.control import ControlType
from core.epanet.hydraulics.control import Control
from core.epanet.hydraulics.link import PumpType
from core.epanet.hydraulics.link import ValveType
from core.epanet.hydraulics.link import FixedStatus
from core.epanet.hydraulics.link import Link
from core.epanet.hydraulics.link import Pipe
from core.epanet.hydraulics.link import Pump
from core.epanet.hydraulics.link import Valve
from core.epanet.hydraulics.link import Status
from core.epanet.hydraulics.node import SourceType
from core.epanet.hydraulics.node import MixingModel
from core.epanet.hydraulics.node import Coordinate
from core.epanet.hydraulics.node import Quality
from core.epanet.hydraulics.node import Junction
from core.epanet.hydraulics.node import Reservoir
from core.epanet.hydraulics.node import Tank
from core.epanet.hydraulics.node import Mixing
from core.epanet.hydraulics.node import Source
from core.epanet.hydraulics.node import Demand
from core.epanet.options.backdrop import BackdropUnits
from core.epanet.options.backdrop import BackdropOptions
from core.epanet.options.energy import PumpEnergyType
from core.epanet.options.energy import EnergyOptions
from core.epanet.options.energy import PumpEnergy
from core.epanet.options.hydraulics import FlowUnits
from core.epanet.options.hydraulics import HeadLoss
from core.epanet.options.hydraulics import Hydraulics
from core.epanet.options.hydraulics import Unbalanced
from core.epanet.options.hydraulics import HydraulicsOptions
from core.epanet.options.options import Options
from core.epanet.options.quality import QualityAnalysisType
from core.epanet.options.quality import QualityOptions
from core.epanet.options.reactions import Reactions
from core.epanet.options.report import StatusWrite
from core.epanet.options.report import ReportOptions
from core.inp_reader_base import SectionReader



class CurveReader(SectionReader):
    """Defines a data curve of X,Y points"""


    @staticmethod
    def read(new_text):
        curve = Curve()
        for line in new_text.splitlines():
            comment_split = str.split(line, ';', 1)
            if len(comment_split) == 2:
                # split curve type from description on colon and set
                colon_split = str.split(line, ':', 1)
                if len(colon_split) == 2:
                    try:
                        curve.setattr_keep_type("curve_type", colon_split[0][1:].strip())
                    except Exception as e:
                        print("Curve could not set curve_type = " + colon_split[0][1:] + '\n' + str(e) + '\n' +
                              str(traceback.print_exc()))
                    curve.description = colon_split[1].strip()
                else:
                    curve.description = line[1:].strip()
                line = comment_split[0].strip()
            if line:
                fields = line.split()
                if len(fields) > 2:
                    curve.curve_id = fields[0]
                    curve.curve_xy.append((fields[1], fields[2]))
        return curve


class LabelReader(SectionReader):
    """A label on the map with location, text, and optional anchor node ID"""


#    attribute,         input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("label",           '', "Text",            '',    '',   '', "Text of label"),
        ('x',               '', "X-Coordinate",    '',    '',   '', "X coordinate of label on study area map"),
        ('y',               '', "Y-Coordinate",    '',    '',   '', "Y coordinate of label on study area map"),
        ('anchor_node_id',  '', "Anchor Node",     '',    '',   '', "ID label of an anchor node (optional)"),
        ('meter_type',      '', "Meter Type",      '',    '',   '', "Type of object being metered by the label"),
        ('meter_id',        '', "Meter ID",        '',    '',   '', "ID of the object (Node or Link) being metered"),
        ("font",            '', "Font",            "",       '', '',  "The label's font"),
        ("size",            '', "Size",            "10.0",   '', '',  "The label's font size"),
        ("bold",            '', "Bold",            "False",  '', '',  "Set to True if the label is to be bold"),
        ("italics",         '', "Italics",         "False",  '', '',  "Set to True if the label is to be italicized"),
    ))

    @staticmethod
    def read(new_text):
        label = Label()
        new_text = SectionReader.set_comment_check_section(label, new_text)
        fields = new_text.split(None, 2)  # Only use split for first two splits, do last one manually below
        if len(fields) > 1:
            (label.x, label.y) = fields[0:2]
            if len(fields) > 2:
                label.label = fields[2]
                if label.label[0] == '"':  # split above would not work with quotes, so find end of label ourselves
                    endquote = label.label.rindex('"')
                    if endquote + 1 < len(label.label):  # If there is more after the label, it is the anchor_node_id
                        label.anchor_node_id = label.label[endquote + 1:].strip()
                        label.label = label.label[0:endquote + 1]
                label.label = label.label.replace('"', '')  # label is quoted in the file, but not while in memory
        return label


class PatternReader:
    """
    Pattern multipliers define how a base quantity is adjusted for each time period.
    If another Pattern is defined with the same ID, it is a continuation of the same Pattern split across lines.
    """
    @staticmethod
    def read(new_text):
        pattern = Pattern()
        for line in new_text.splitlines():
            comment_split = str.split(line, ';', 1)
            if len(comment_split) == 2:
                pattern.description += line[1:].strip()
                line = comment_split[0].strip()
            if line:
                fields = line.split()
                if len(fields) > 1:
                    pattern.pattern_id = fields[0]
                    pattern.multipliers.extend(fields[1:])
        return pattern


class TitleReader(SectionReader):
    """EPANET descriptive title"""

    SECTION_NAME = "[TITLE]"

    @staticmethod
    def read(new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        title = Title()
        lines = new_text.replace(title.SECTION_NAME, '').strip().splitlines()
        if len(lines) > 0:
            title.title = lines[0]
        if len(lines) > 1:
            title.notes = '\n'.join(lines[1:])
        return title


class ControlReader():
    """Defines simple controls that modify links based on a single condition"""
    @staticmethod
    def read(new_text):
        control = Control()
        fields = new_text.split()
        control.link_id, control.status = fields[1], fields[2]
        type_str = fields[4].upper()
        if type_str == "NODE":
            control.node_id = fields[5]
            control.control_type = ControlType[fields[6].upper()]
            control.value = fields[7]
        elif type_str == "TIME":
            control.control_type = ControlType.TIME
            control.time = fields[5]
        elif type_str == "CLOCKTIME":
            control.control_type = ControlType.CLOCKTIME
            control.clocktime = ' '.join(fields[5:])
        else:
            raise NameError("Unable to parse Control: " + new_text)
        return control


class LinkReader(SectionReader):
    """A link in an EPANET model"""


    @staticmethod
    def read(new_text):
        link = Link()
        new_text = SectionReader.set_comment_check_section(link, new_text)
        fields = new_text.split(None, 3)
        if len(fields) > 2:
            (link.id, link.inlet_node, link.outlet_node) = fields[0:3]
            if len(fields) > 3:
                link.description = fields[3]
        return link


class PipeReader(Link):
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

    @staticmethod
    def read(new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        pipe = Pipe()
        new_text = SectionReader.set_comment_check_section(pipe, new_text)
        fields = new_text.split(None, 8)
        if len(fields) > 2:
            pipe.id, pipe.inlet_node, pipe.outlet_node = fields[0:3]
        if len(fields) > 6:
            pipe.length = fields[3]
            pipe.diameter = fields[4]
            pipe.roughness = fields[5]
            pipe.loss_coefficient = fields[6]
        if len(fields) > 7:
            pipe.initial_status = fields[7]
        return pipe


class PumpReader(Link):
    """A Pump link in an EPANET model"""


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

    @staticmethod
    def read(new_text):
        pump = Pump()
        new_text = SectionReader.set_comment_check_section(pump, new_text)
        fields = new_text.split()
        if len(fields) > 2:
            pump.id, pump.inlet_node, pump.outlet_node = fields[0:3]
            for key_index in range(3, len(fields) - 1, 2):
                value_index = key_index + 1
                if fields[key_index].upper() == "HEAD":
                    pump.type = PumpType.HEAD
                    pump.head_curve_id = fields[value_index]
                elif fields[key_index].upper() == "POWER":
                    pump.type = PumpType.POWER
                    pump.power = fields[value_index]
                elif fields[key_index].upper() == "PATTERN":
                    pump.pattern = fields[value_index]
                elif fields[key_index].upper() == "SPEED":
                    pump.speed = fields[value_index]
        return pump


class ValveReader(Link):
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
        ("setting",                '', "Setting",            "",    '', '', "Pressure for PRV, PSV, and PBV; flow for FCV, Loss Coefficient for TCV, head loss curve ID for GPV"),
        ("minor_loss_coefficient", '', "Loss Coeff.",        "",    '', '', "TCV (throttle control valve) Loss Coefficient"),
        ("status",                 '', "Fixed Status",       "",    '', '', "Initial status of a valve"),
    ))

    @staticmethod
    def read(new_text):
        valve = Valve()
        new_text = SectionReader.set_comment_check_section(valve, new_text)
        fields = new_text.split()
        if len(fields) > 2:
            valve.id = fields[0]
            valve.inlet_node = fields[1]
            valve.outlet_node = fields[2]
            if len(fields) > 3:
                valve.diameter = fields[3]
            if len(fields) > 4:
                valve.type = ValveType[fields[4].upper()]
            if len(fields) > 5:
                valve.setting = fields[5]
            if len(fields) > 6:
                valve.minor_loss_coefficient = fields[6]
        return valve


class StatusReader(SectionReader):
    """
        Initial status of a link at the start of the simulation.
        Pipes can have a status of OPEN, CLOSED, or CV.
        Pumps can have a status of OPEN, CLOSED, or a speed.
    """


    @staticmethod
    def read(new_text):
        status = Status()
        new_text = SectionReader.set_comment_check_section(status, new_text)
        fields = new_text.split()
        if len(fields) > 1:
            status.id = fields[0]
            status.status = fields[1]
        return status


class CoordinateReader(SectionReader):

    @staticmethod
    def read(new_text):
        coordinate = Coordinate()
        (coordinate.id, coordinate.x, coordinate.y) = new_text.split()
        return coordinate


class QualityReader(SectionReader):
    """Initial water quality at a node."""


    @staticmethod
    def read(new_text):
        quality = Quality()
        (quality.id, quality.initial_quality) = new_text.split()
        return quality


class JunctionReader(SectionReader):
    """Junction properties"""


    #    attribute, input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("id",            '', "Name",            '',   '',   '', "User-assigned name of junction"),
        ('',                '', "X-Coordinate",    '',   '',   '', "X coordinate of junction on study area map"),
        ('',                '', "Y-Coordinate",    '',   '',   '', "Y coordinate of junction on study area map"),
        ('',                '', "Description",     '',   '',   '', "Optional comment or description"),
        ('',                '', "Tag",             '',   '',   '', "Optional category or classification"),
        ('elevation',       '', "Elevation",       '',   '',   '', "Elevation of junction"),
        ('base_demand_flow',    '', 'Base Demand',       '',  '',   '', "Base demand flow, characteristic of all demands at this node"),
        ('demand_pattern_id',   '', 'Demand Pattern',    '',  '',   '', "Demand pattern ID, optional"),
        ('demand_categories',   '', 'Demand Categories', '',  '',   '', "Number of demand categories, click to edit"),
        ('emitter_coefficient', '', 'Emitter Coeff.',    '',  '',   '', "Emitters are used to model flow through sprinkler heads or pipe leaks. Flow out of the emitter equals the product of the flow coefficient and the junction pressure raised to EMITTER EXPONENT, which defaults to 0.5 and can be set in OPTIONS section."),
        ('initial_quality',     '', 'Initial Quality',   '',  '',   '', "Water quality level at the junction at the start of the simulation period"),
        ('source_quality',      '', 'Source Quality',    '',  '',   '', "Quality of any water entering the network at this location, click to edit")))

    @staticmethod
    def read(new_text):
        junction = Junction()
        new_text = SectionReader.set_comment_check_section(junction, new_text)
        fields = new_text.split()
        if len(fields) > 0:
            junction.id = fields[0]
        if len(fields) > 1:
            junction.elevation = fields[1]
        if len(fields) > 2:
            junction.base_demand_flow = fields[2]
        if len(fields) > 3:
            junction.demand_pattern_id = fields[3]
        return junction


class ReservoirReader(SectionReader):
    """Reservoir properties"""


#    attribute, input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("id",              '', "Name",            '',    '',   '', "User-assigned name of reservior"),
        ('',                '', "X-Coordinate",    '',    '',   '', "X coordinate of reservior on study area map"),
        ('',                '', "Y-Coordinate",    '',    '',   '', "Y coordinate of reservior on study area map"),
        ('',                '', "Description",     '',    '',   '', "Optional comment or description"),
        ('',                '', "Tag",             '',    '',   '', "Optional category or classification"),
        ('total_head',      '', "Total Head",      '0.0', '',   '', "Hydraulic head (elevation + pressure head) of water in the reservoir"),
        ('head_pattern_id', '', 'Head Pattern',    '',    '',   '', "Head pattern ID, can be used to make the reservoir head vary with time"),
        ('initial_quality', '', 'Initial Quality', '',    '',   '', "Water quality level at the reservior at the start of the simulation period"),
        ('source_quality',  '', 'Source Quality',  '',    '',   '', "Quality of any water entering the network at this location, click to edit")))

    @staticmethod
    def read(new_text):
        reservoir = Reservoir()
        new_text = SectionReader.set_comment_check_section(reservoir, new_text)
        fields = new_text.split()
        if len(fields) > 0:
            reservoir.id = fields[0]
        if len(fields) > 1:
            reservoir.total_head = fields[1]
        if len(fields) > 2:
            reservoir.head_pattern_id = fields[2]
        return reservoir


class TankReader(SectionReader):
    """Tank properties"""


#    attribute, input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("id",              '', "Name",            '',    '',   '', "User-assigned name of tank"),
        ('',                '', "X-Coordinate",    '',    '',   '', "X coordinate of tank on study area map"),
        ('',                '', "Y-Coordinate",    '',    '',   '', "Y coordinate of tank on study area map"),
        ('',                '', "Description",     '',    '',   '', "Optional comment or description"),
        ('',                '', "Tag",             '',    '',   '', "Optional category or classification"),
        ('elevation',       '', "Elevation",       '0.0', '',   '', "Elevation of tank"),
        ('initial_level',   '', "Initial Level",   '0.0', '',   '', "Height of the water surface above the bottom elevation of the tank at the start of the simulation."),
        ('minimum_level',   '', "Minimum Level",   '0.0', '',   '', "Minimum height in feet (meters) of the water surface above the bottom elevation that will be maintained."),
        ('maximum_level',   '', "Maximum Level",   '0.0', '',   '', "Maximum height in feet (meters) of the water surface above the bottom elevation that will be maintained."),
        ('diameter',        '', "Diameter",        '0.0', '',   '', "The diameter of the tank"),
        ('minimum_volume',  '', "Minimum Volume",  '0.0', '',   '', "The volume of water in the tank when it is at its minimum level"),
        ('volume_curve',    '', "Volume Curve",    '',    '',   '', "The ID label of a curve used to describe the relation between tank volume and water level"),
        ('mixing_model',    '', "Mixing Model",    '',    '',   '', "The type of water quality mixing that occurs within the tank"),
        ('mixing_fraction', '', "Mixing Fraction", '0.0', '',   '', "The fraction of the tank's total volume that comprises the inlet-outlet compartment of the two-compartment (2COMP) mixing model"),
        ('reaction_coeff',  '', "Reaction Coeff.", '',    '',   '', "Tank-specific reaction coefficient"),
        ('initial_quality', '', 'Initial Quality', '0.0', '',   '', "Water quality level in the tank at the start of the simulation period"),
        ('source_quality',  '', 'Source Quality',  '',    '',   '', "Quality of any water entering the network at this location, click to edit")))

    @staticmethod
    def read(new_text):
        tank = Tank()
        new_text = SectionReader.set_comment_check_section(tank, new_text)
        fields = new_text.split()
        if len(fields) > 0:
            tank.id = fields[0]
        if len(fields) > 1:
            tank.elevation = fields[1]
        if len(fields) > 2:
            tank.initial_level = fields[2]
        if len(fields) > 3:
            tank.minimum_level = fields[3]
        if len(fields) > 4:
            tank.maximum_level = fields[4]
        if len(fields) > 5:
            tank.diameter = fields[5]
        if len(fields) > 6:
            tank.minimum_volume = fields[6]
        if len(fields) > 7:
            tank.volume_curve = fields[7]
        return tank


class MixingReader(SectionReader):
    """Mixing model and volume fraction of a Tank"""


    @staticmethod
    def read(new_text):
        mixing = Mixing()
        new_text = SectionReader.set_comment_check_section(mixing, new_text)
        fields = new_text.split()
        if len(fields) > 0:
            mixing.id = fields[0]
        if len(fields) > 1:
            mixing.mixing_model = MixingModel[fields[1].upper().replace("2", "TWO_")]
        if len(fields) > 2:
            mixing.mixing_fraction = fields[2]
        return mixing


class SourceReader(SectionReader):
    """Defines locations of water quality sources"""


    @staticmethod
    def read(new_text):
        source = Source()
        fields = new_text.split()
        if len(fields) > 0:
            source.id = fields[0]
        if len(fields) > 1:
            source.source_type = SourceType[fields[1].upper()]
        if len(fields) > 2:
            source.baseline_strength = fields[2]
        if len(fields) > 3:
            source.pattern_id = fields[3]
        return source


class DemandReader(SectionReader):
    """Define multiple water demands at junction nodes"""


    @staticmethod
    def read(new_text):
        demand = Demand()
        fields = new_text.split()
        if len(fields) > 0:
            demand.junction_id = fields[0]
        if len(fields) > 1:
            demand.base_demand = fields[1]
        if len(fields) > 2:
            demand.demand_pattern = fields[2]
        if len(fields) > 3:
            demand.category = fields[3]
        return demand


class BackdropOptionsReader(SectionReader):
    """Identifies a backdrop image and dimensions for the network map"""

    SECTION_NAME = "[BACKDROP]"

    @staticmethod
    def read(new_text):
        backdrop_options = BackdropOptions()
        for line in new_text.splitlines():
            try:
                line = SectionReader.set_comment_check_section(backdrop_options, line)
                fields = line.split()
                if len(fields) > 1:
                    if fields[0].lower() == "dimensions" and len(fields) > 4:
                        backdrop_options.dimensions = fields[1:5]
                    elif fields[0].lower() == "offset" and len(fields) > 2:
                        backdrop_options.offset = (fields[1], fields[2])
                    else:
                        backdrop_options.setattr_keep_type(Project.format_as_attribute_name(fields[0]), fields[1])
            except:
                print("BackdropOptions skipping input line: " + line)
        return backdrop_options


class EnergyOptionsReader(SectionReader):
    """Defines global parameters used to compute pumping energy and cost"""

    SECTION_NAME = "[ENERGY]"

    #    attribute,            input_name, label, default, english, metric, hint
    metadata = Metadata((
        ("global_efficiency", "Global Efficiency"),
        ("global_price", "Global Price"),
        ("global_pattern", "Global Pattern"),
        ("demand_charge", "Demand Charge")))
    """Mapping between attribute name and name used in input file"""

    @staticmethod
    def read(new_text):
        energy_options = EnergyOptions()
        for line in new_text.splitlines():
            try:
                line = SectionReader.set_comment_check_section(energy_options, line)
                fields = line.split()
                if len(fields) > 1:
                    if fields[0].upper() == "PUMP":
                        energy_options.pumps.append(PumpEnergy(line))
                    else:
                        SectionReader.set_text_line(energy_options, line)
            except:
                print("BackdropOptions skipping input line: " + line)
        return energy_options


class PumpEnergyReader(SectionReader):
    """Parameters used to compute pumping energy and cost for a particular pump"""

    @staticmethod
    def read(new_text):
        pump_energy = PumpEnergy()
        new_text = SectionReader.set_comment_check_section(pump_energy, new_text)
        fields = new_text.split()
        if len(fields) > 3:
            pump_energy.id = fields[1]
            pump_energy.PricePatternEfficiency = PumpEnergyType[fields[2].upper()]
            pump_energy.value = fields[3]
        return pump_energy


class HydraulicsOptionsReader(SectionReader):
    """EPANET Hydraulics Options"""

    SECTION_NAME = "[OPTIONS]"

    #    attribute,             input_name, label, default, english, metric, hint
    metadata = Metadata((
        ("flow_units",          "Units"),
        ("head_loss",           "Headloss"),
        ("specific_gravity",    "Specific Gravity"),
        ("viscosity",           "Viscosity"),
        ("maximum_trials",      "Trials"),
        ("accuracy",            "Accuracy"),
        ("check_frequency",     "CHECKFREQ"),
        ("max_check",           "MAXCHECK"),
        ("damp_limit",          "DAMPLIMIT"),
        ("unbalanced_continue", "Unbalanced"),
        ("default_pattern",     "Pattern"),
        ("demand_multiplier",   "Demand Multiplier"),
        ("emitter_exponent",    "Emitter Exponent"),
        ("",                    "Quality"),
        ("",                    "Diffusivity"),
        ("",                    "Tolerance")))
    """Mapping between attribute name and name used in input file"""

    @staticmethod
    def read(new_text):
        hydraulics_options = HydraulicsOptions()
        for line in new_text.splitlines():
            try:
                line = line.strip()
                if not line.startswith((';', '[')):
                    lower_line = line.lower()
                    if lower_line:
                        for meta_item in hydraulics_options.metadata:
                            key = meta_item.input_name.lower()
                            if len(lower_line) > len(key):
                                if lower_line.startswith(key) and lower_line[len(key)] in (' ', '\t'):
                                    if meta_item.attribute == "unbalanced_continue":
                                        fields = line.split()
                                        hydraulics_options.unbalanced = Unbalanced[fields[1].upper()]
                                        if len(fields) > 2:
                                            hydraulics_options.unbalanced_continue = fields[2]
                                    else:
                                        attr_value = line[len(key) + 1:].strip()
                                        hydraulics_options.setattr_keep_type(meta_item.attribute, attr_value)
            except:
                print("HydraulicsOptions skipping input line: " + line)
        return hydraulics_options


class OptionsReader(SectionReader):
    """EPANET Options"""

    SECTION_NAME = "[OPTIONS]"

    section_comments = (";; Hydraulics", ";; Water Quality")

    @staticmethod
    def read(new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        options = Options()
        # Skip the comments we insert automatically
        for comment in Options.section_comments:
            new_text = new_text.replace(comment + '\n', '')
        options.hydraulics.set_text(new_text)
        options.quality.set_text(new_text)
        for line in new_text.splitlines():
            line_list = line.split()
            if line_list:
                if str(line_list[0]).strip().upper() == "MAP":
                    options.map = ' '.join(line_list[1:])
        return options


class QualityOptionsReader(SectionReader):
    """EPANET Quality Options"""

    SECTION_NAME = "[OPTIONS]"


    @staticmethod
    def read(new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        quality_options = QualityOptions()
        quality_options.quality = QualityAnalysisType.NONE  # default to NONE until found below
        quality_options.chemical_name = ""
        quality_options.mass_units = ""
        quality_options.trace_node = ""

        for line in new_text.splitlines():
            line_list = line.split()
            if line_list:
                if str(line_list[0]).strip().upper() == "QUALITY":
                    quality_type = str(line_list[1]).strip().upper()
                    try:
                        quality_options.quality = QualityAnalysisType[quality_type]
                    except:
                        quality_options.quality = QualityAnalysisType.CHEMICAL
                        quality_options.chemical_name = str(line_list[1])
                    if quality_options.quality == QualityAnalysisType.TRACE:
                        quality_options.trace_node = line_list[2]
                    elif len(line_list) > 2:
                        quality_options.mass_units = line_list[2]
                elif str(line_list[0]).strip().upper() == "DIFFUSIVITY":
                    quality_options.diffusivity = float(line_list[1])
                elif str(line_list[0]).strip().upper() == "TOLERANCE":
                    quality_options.tolerance = float(line_list[1])
        return quality_options


class ReactionsReader(SectionReader):
    """Defines parameters related to chemical reactions occurring in the network"""

    SECTION_NAME = "[REACTIONS]"

    #    attribute,               input_name, label, default, english, metric, hint
    metadata = Metadata((
        ("order_bulk",            "Order Bulk"),
        ("order_wall",            "Order Wall"),
        ("order_tank",            "Order Tank"),
        ("global_bulk",           "Global Bulk"),
        ("global_wall",           "Global Wall"),
        ("limiting_potential",    "Limiting Potential"),
        ("roughness_correlation", "Roughness Correlation")))
    """Mapping between attribute name and name used in input file"""

    @staticmethod
    def read(new_text):
        """Read properties from text.
            Args:
                new_text (str): Text to parse into properties.
        """
        reactions = Reactions()
        # Replace "zero" (any capitalization) with numeral 0
        zero_pos = new_text.upper().find("ZERO")
        while zero_pos >= 0:
            new_text = new_text[:zero_pos] + '0' + new_text[zero_pos + len("ZERO"):]
            zero_pos = new_text.upper().find("ZERO", zero_pos)
        for line in new_text.splitlines():
            upper_line = line.upper().strip()
            if upper_line.startswith("BULK") or upper_line.startswith("WALL") or upper_line.startswith("TANK"):
                reactions.comment += '\n' + line  # TODO: parse into table of per pipe values
            else:
                SectionReader.set_text_line(reactions, line)
        return reactions


class ReportOptionsReader(SectionReader):
    """Report Options"""

    SECTION_NAME = "[REPORT]"

    #     attribute, input_name
    metadata = Metadata((
        ("status",   "Status"),
        ("summary",  "Summary"),
        ("pagesize", "Page"),
        ("energy",   "Energy"),
        ("file",     "File")))

    metadata_lists = Metadata((
        ("nodes",   "Nodes"),
        ("links",   "Links"),
        ("elevation", "Elevation"),
        ("demand", "Demand"),
        ("head", "Head"),
        ("pressure", "Pressure"),
        ("quality", "Quality"),
        ("length", "Length"),
        ("diameter", "Diameter"),
        ("flow", "Flow"),
        ("velocity", "Velocity"),
        ("headloss", "Headloss"),
        ("position", "Position"),
        ("setting", "Setting"),
        ("reaction", "Reaction"),
        ("friction_factor", "F-Factor")))
    """Mapping between attribute name and name used in input file"""

    # @staticmethod
    # def read(new_text):
    #     """Read this section from the text representation"""
    #     Section.set_text(report_options, new_text)  # Initialize, and set values using metadata
    #     # Custom code to set nodes and links since they may be split across lines
    #     report_options.nodes = []
    #     report_options.links = []
    #     for line in new_text.splitlines():
    #         (attr_name, attr_value) = new_text.split(None, 1)
    #         attr_name = attr_name.upper()
    #         if attr_name == "NODES":
    #             report_options.nodes.extend(attr_value.split())
    #         elif attr_name == "LINKS":
    #             report_options.links.extend(attr_value.split())
    #         elif attr_name in ()
    #         elif attr_name == "STATUS":
    #             report_options.status = attr_value
    #         elif attr_name == "SUMMARY":
    #             report_options.setattr_keep_type("summary", attr_value)
    #         elif attr_name == "PAGESIZE" or attr_name == "PAGE":
    #             report_options.pagesize = attr_value
    #         elif attr_name == "ENERGY":
    #             report_options.setattr_keep_type("energy", attr_value)
    #         else:
    #             report_options.parameters.extend(line)
    #    return report_options

    @staticmethod
    def read(new_text):
        """Set this section from text.
            Args:
                line (str): One line of text formatted as input file.
        """
        report_options = ReportOptions()
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(report_options, line)
            if line.strip():
                # Set fields from metadata
                (attr_name, attr_value) = SectionReader.get_attr_name_value(report_options, line)
                if attr_name:  # Set fields from metadata
                    try:
                        report_options.setattr_keep_type(attr_name, attr_value)
                        return
                    except:
                        print("Section report could not set " + attr_name)
                else:
                    report_options.parameters.append(line)
        return report_options

