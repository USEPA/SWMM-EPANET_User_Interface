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
from core.inp_writer_base import SectionWriter



class CurveWriter(SectionWriter):
    """Defines a data curve of X,Y points"""

    field_format = " {:16}\t{:12}\t{:12}\n"

    @staticmethod
    def as_text(curve):
        """format contents of this item for writing to file"""
        inp = ''
        if curve.curve_type != CurveType.UNSET:
            inp += ";{}: {}\n".format(curve.curve_type.name, curve.description)
        elif curve.description:
            inp += ";{}\n".format(curve.description)
        for xy in curve.curve_xy:
            inp += CurveWriter.field_format.format(curve.curve_id, xy[0], xy[1])
        return inp



class LabelWriter(SectionWriter):
    """A label on the map with location, text, and optional anchor node ID"""

    field_format = '{:16}\t{:16}\t"{}"\t{:16}'

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
    def as_text(label):
        """format contents of this item for writing to file"""
        return LabelWriter.field_format.format(label.x, label.y, label.label, label.anchor_node_id)



class PatternWriter:
    """
    Pattern multipliers define how a base quantity is adjusted for each time period.
    If another Pattern is defined with the same ID, it is a continuation of the same Pattern split across lines.
    """
    @staticmethod
    def as_text(pattern):
        """format contents of this item for writing to file"""
        count = 6
        section_text = ""
        for line in pattern.description.splitlines(True):
            section_text += ';' + line
        for multiplier in pattern.multipliers:
            if count == 6:        # add ID to first line and break lines before they get too long
                if section_text:  # If there are already values added, put next value on a new line
                    section_text += '\n'
                section_text += " {:16}".format(pattern.pattern_id)
                count = 0
            section_text += "\t{:12}".format(multiplier)
            count += 1
        return section_text



class TitleWriter(SectionWriter):
    """EPANET descriptive title"""

    SECTION_NAME = "[TITLE]"

    @staticmethod
    def as_text(title):
        """format contents of this item for writing to file"""
        return Title.SECTION_NAME + '\n' + title.title + '\n' + title.notes



class ControlWriter():
    """Defines simple controls that modify links based on a single condition"""
    @staticmethod
    def as_text(control):
        """format contents of this item for writing to file"""
        if control.link_id:
            prefix = " LINK " + control.link_id + ' ' + control.status
            if control.control_type == ControlType.ABOVE or control.control_type == ControlType.BELOW:
                return prefix + " IF NODE " + control.node_id + ' ' + control.control_type.name + ' ' + str(control.value)
            elif control.control_type == ControlType.TIME and len(control.time) > 0:
                return prefix + " AT TIME " + control.time
            elif control.control_type == ControlType.CLOCKTIME and len(control.clocktime) > 0:
                return prefix + " AT CLOCKTIME " + control.clocktime
        return ''



class LinkWriter(SectionWriter):
    """A link in an EPANET model"""

    field_format = "{:16}\t{:16}\t{:16}"

    @staticmethod
    def as_text(link):
        """format contents of this item for writing to file"""
        if len(link.id) > 0:
            return LinkWriter.field_format.format(link.id, link.inlet_node, link.outlet_node)  # link.description
        elif link.comment:
            return link.comment



class PipeWriter(Link):
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

    @staticmethod
    def as_text(pipe):
        """format contents of this item for writing to file"""
        if len(pipe.id) > 0:
            return PipeWriter.field_format.format(pipe.id, pipe.inlet_node, pipe.outlet_node, pipe.length, pipe.diameter,
                                            pipe.roughness, pipe.loss_coefficient, pipe.initial_status, pipe.comment)
        elif pipe.comment:
            return pipe.comment



class PumpWriter(Link):
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

    @staticmethod
    def as_text(pump):
        """format contents of this item for writing to file"""
        if len(pump.id) > 0:
            txt = PumpWriter.field_format.format(pump.id, pump.inlet_node, pump.outlet_node)
            if pump.type == PumpType.HEAD:
                txt += "\tHEAD " + pump.head_curve_id
            else:
                txt += "\tPOWER " + pump.power
            if pump.pattern:
                txt += "\tPATTERN " + pump.pattern
            if pump.speed != "0.0":
                txt += "\tSPEED " + pump.speed
            if pump.comment:
                comment_stripped = pump.comment.replace(';', '').strip()
                if comment_stripped:
                    txt += "\t; " + comment_stripped
            return txt
        elif pump.comment:
            return pump.comment



class ValveWriter(Link):
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

    @staticmethod
    def as_text(valve):
        """format contents of this item for writing to file"""
        if len(valve.id) > 0:
            return ValveWriter.field_format.format(valve.id,
                                            valve.inlet_node,
                                            valve.outlet_node,
                                            valve.diameter,
                                            valve.type.name,
                                            valve.setting,
                                            valve.minor_loss_coefficient,
                                            valve.comment)
        elif valve.comment:
            return valve.comment



class StatusWriter(SectionWriter):
    """
        Initial status of a link at the start of the simulation.
        Pipes can have a status of OPEN, CLOSED, or CV.
        Pumps can have a status of OPEN, CLOSED, or a speed.
    """

    field_format = "{:16}\t{}\t{}"

    @staticmethod
    def as_text(status):
        """format contents of this item for writing to file"""
        if len(status.id) > 0:
            return StatusWriter.field_format.format(status.id,
                                            status.status,
                                            status.comment)
        elif status.comment:
            return status.comment



class CoordinateWriter(SectionWriter):
    field_format = "{:16}\t{:16}\t{:16}"

    @staticmethod
    def as_text(coordinate):
        """format contents of this item for writing to file"""
        return CoordinateWriter.field_format.format(coordinate.id, coordinate.x, coordinate.y)



class QualityWriter(SectionWriter):
    """Initial water quality at a node."""

    field_format = "{:16}\t{}"

    @staticmethod
    def as_text(quality):
        """format contents of this item for writing to file"""
        return QualityWriter.field_format.format(quality.id, quality.initial_quality)



class JunctionWriter(SectionWriter):
    """Junction properties"""

    field_format = "{:16}\t{:6}\t{:6}\t{:7}"

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
    def as_text(junction):
        """format contents of this item for writing to file"""
        return JunctionWriter.field_format.format(junction.id, junction.elevation, junction.base_demand_flow, junction.demand_pattern_id)



class ReservoirWriter(SectionWriter):
    """Reservoir properties"""

    field_format = "{:16}\t{:6}\t{:6}\t{}"

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
    def as_text(reservoir):
        """format contents of this item for writing to file"""
        return ReservoirWriter.field_format.format(reservoir.id, reservoir.total_head, reservoir.head_pattern_id, reservoir.comment)



class TankWriter(SectionWriter):
    """Tank properties"""

    field_format = " {:16}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:16}\t{}"

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
    def as_text(tank):
        """format contents of this item for writing to file"""
        return TankWriter.field_format.format(tank.id, tank.elevation, tank.initial_level,
                                        tank.minimum_level, tank.maximum_level, tank.diameter,
                                        tank.minimum_volume, tank.volume_curve, tank.comment)



class MixingWriter(SectionWriter):
    """Mixing model and volume fraction of a Tank"""

    field_format = "{:16}\t{:12}\t{:12}\t{}"

    @staticmethod
    def as_text(mixing):
        """format contents of this item for writing to file"""
        return MixingWriter.field_format.format(mixing.id,
                                        mixing.mixing_model.name.replace("TWO_", "2"),
                                        mixing.mixing_fraction,
                                        mixing.comment)



class SourceWriter(SectionWriter):
    """Defines locations of water quality sources"""

    field_format = "{:16}\t{:14}\t{:12}\t{}"

    @staticmethod
    def as_text(source):
        inp = ''
        if source.comment:
            inp = source.comment + '\n'
        inp += SourceWriter.field_format.format(source.id,
                                        source.source_type.name,
                                        source.baseline_strength,
                                        source.pattern_id)
        return inp



class DemandWriter(SectionWriter):
    """Define multiple water demands at junction nodes"""

    field_format = "{:16}\t{:9}\t{:10}\t{}"

    @staticmethod
    def as_text(demand):
        inp = ''
        if demand.comment:
            inp = demand.comment + '\n'
        inp += DemandWriter.field_format.format(demand.junction_id,
                                        demand.base_demand,
                                        demand.demand_pattern,
                                        demand.category)
        return inp



class BackdropOptionsWriter(SectionWriter):
    """Identifies a backdrop image and dimensions for the network map"""

    SECTION_NAME = "[BACKDROP]"

    @staticmethod
    def as_text(backdrop_options):
        if backdrop_options.file:
            text_list = [BackdropOptions.SECTION_NAME]
            if backdrop_options.dimensions:
                text_list.append(" {:17}\t{:16}\t{:16}\t{:16}\t{:16}".format("DIMENSIONS",
                                 backdrop_options.dimensions[0], backdrop_options.dimensions[1], backdrop_options.dimensions[2], backdrop_options.dimensions[3]))
            if backdrop_options.units is not None:
                if isinstance(backdrop_options.units, Enum):
                    units_name = backdrop_options.units.name
                else:
                    units_name = str(backdrop_options.units)
                text_list.append(" {:17}\t{}".format("UNITS", units_name))
            if backdrop_options.file:
                text_list.append(" {:17}\t{}".format("FILE", backdrop_options.file))
            if backdrop_options.offset and len(backdrop_options.offset) > 1:
                text_list.append(" {:17}\t{:16}\t{:16}".format("OFFSET", backdrop_options.offset[0], backdrop_options.offset[1]))
            return '\n'.join(text_list)
        else:
            return ''



class EnergyOptionsWriter(SectionWriter):
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
    def as_text(energy_options):
        if energy_options.global_efficiency == "75" \
           and energy_options.global_price == "0.0" \
           and energy_options.global_pattern == '' \
           and energy_options.demand_charge == "0.0" \
           and len(energy_options.pumps) == 0:
            return ''  # This section has nothing different from defaults, return blank
        else:
            txt = [SectionWriter.as_text(energy_options)]
            for pump_energy in energy_options.pumps:      # Add text for each pump energy
                txt.append(pump_energy.as_text())
            return '\n'.join(txt)



class PumpEnergyWriter(SectionWriter):
    """Parameters used to compute pumping energy and cost for a particular pump"""

    field_format = "PUMP {:16}\t{:8}\t{}\t{}"

    @staticmethod
    def as_text(pump_energy):
        """format contents of this item for writing to file"""
        if len(pump_energy.id) > 0:
            return PumpEnergyWriter.field_format.format(pump_energy.id,
                                            pump_energy.PricePatternEfficiency.name,
                                            pump_energy.value,
                                            pump_energy.comment)
        elif pump_energy.comment:
            return pump_energy.comment



class HydraulicsOptionsWriter(SectionWriter):
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
    def as_text(hydraulics_options):
        text_list = []
        for meta_item in HydraulicsOptions.metadata:
            attr_value = ""
            if meta_item.input_name == "Unbalanced":
                if hydraulics_options.unbalanced == Unbalanced.STOP:
                    attr_value = "STOP"
                else:
                    attr_value = "Continue " + str(hydraulics_options.unbalanced_continue)
            if attr_value:
                text_list.append(HydraulicsOptionsWriter.field_format.format(meta_item.input_name, attr_value))
            else:
                attr_line = HydraulicsOptionsWriter._get_attr_line(hydraulics_options,
                                                                   meta_item.input_name,
                                                                   meta_item.attribute)
                if attr_line:
                    text_list.append(attr_line)
        return '\n'.join(text_list)



class OptionsWriter(SectionWriter):
    """EPANET Options"""

    SECTION_NAME = "[OPTIONS]"

    section_comments = (";; Hydraulics", ";; Water Quality")

    @staticmethod
    def as_text(options):
        """Contents of this item formatted for writing to file"""
        text_list = [options.SECTION_NAME]
        if options.map:
            text_list.append(" MAP                \t" + options.map)
        if options.hydraulics is not None:
            text_list.append(Options.section_comments[0])
            text_list.append(HydraulicsOptionsWriter.as_text(options.hydraulics))
        if options.quality is not None:
            text_list.append(Options.section_comments[1])
            text_list.append(QualityOptionsWriter.as_text(options.quality))
        return '\n'.join(text_list)



class QualityOptionsWriter(SectionWriter):
    """EPANET Quality Options"""

    SECTION_NAME = "[OPTIONS]"

    field_format = " {:20}\t{}\n"

    @staticmethod
    def as_text(quality_options):
        """Contents of this item formatted for writing to file"""
        txt = " Quality            \t"
        if quality_options.quality is None or quality_options.quality == QualityAnalysisType.NONE:
            txt = ""
        elif quality_options.quality == QualityAnalysisType.AGE:
            txt += "AGE"
        elif quality_options.quality == QualityAnalysisType.TRACE:
            txt += "Trace"
            if quality_options.trace_node:
                txt += " " + quality_options.trace_node
        elif quality_options.quality == QualityAnalysisType.CHEMICAL:
            if quality_options.chemical_name:
                txt += quality_options.chemical_name
            else:
                txt += "CHEMICAL"
        if txt and quality_options.mass_units:
            txt += " " + quality_options.mass_units
        if txt:
            txt += "\n"
        txt += QualityOptionsWriter.field_format.format("Diffusivity", str(quality_options.diffusivity))
        txt += QualityOptionsWriter.field_format.format("Tolerance", str(quality_options.tolerance))
        return txt



class ReactionsWriter(SectionWriter):
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

    # @staticmethod
    # def as_text(reactions):
    #     """format contents of this item for writing to file"""
    #     if reactions.comment and reactions.comment.upper().startswith(";TYPE"):
    #         # TODO: implement reactions table as list of reactions
    #         return reactions.value
    #     else:
    #         return SectionWriter.as_text(reactions)



class ReportOptionsWriter(SectionWriter):
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

    @staticmethod
    def as_text(report_options):
        txt = SectionWriter.as_text(report_options)
        try:
            if report_options.parameters:
                txt += '\n' + '\n'.join(report_options.parameters)
        except:
            pass
        return txt
    #     # [report_options.SECTION_NAME]
    #     # report_options._get_attr_line("Status", "status")
    #     # Section.__getattribute__()
    #     # txt.append("Status\t" + report_options.status.name)
    #     # if report_options.file:
    #     #     txt.append("File\t" + str(report_options.file))
    #     # if report_options.pagesize:
    #     #     txt.append("Pagesize\t" + str(report_options.pagesize))
    #     # if report_options.pagesize:
    #     #     txt.append("Pagesize\t" + str(report_options.pagesize))
    #     # if report_options.file:
    #     #     txt.append("File\t" + str(report_options.file))
    #     # txt.append(SectionWriter.as_text(report_options))  # Get text for the global variables using metadata
    #     if report_options.nodes:
    #         txt += '\n' + ReportOptionsWriter.field_format.format("Nodes", ' '.join()
    #     return '\n'.join(txt)


