import traceback
from enum import Enum
from core.project_base import Section
from core.epanet.curves import CurveType
from core.epanet.curves import Curve
from core.epanet.labels import MeterType
from core.epanet.labels import Label
from core.epanet.patterns import Pattern
from core.epanet.title import Title
from core.epanet.hydraulics.control import ControlType
from core.epanet.hydraulics.control import Control
from core.epanet.hydraulics.control import Rule
from core.epanet.hydraulics.link import ValveType
from core.epanet.hydraulics.link import FixedStatus
from core.epanet.hydraulics.link import Pipe
from core.epanet.hydraulics.link import Pump
from core.epanet.hydraulics.link import Valve
from core.epanet.hydraulics.link import Status
from core.epanet.hydraulics.node import SourceType
from core.epanet.hydraulics.node import MixingModel
from core.coordinate import Coordinate
from core.epanet.hydraulics.node import Junction
from core.epanet.hydraulics.node import Reservoir
from core.epanet.hydraulics.node import Tank
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
from core.utility import ParseData


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
            inp += CurveWriter.field_format.format(curve.name, xy[0], xy[1])
        return inp


class LabelWriter(SectionWriter):
    """A label on the map with location, text, and optional anchor node ID"""

    field_format = u'{:16}\t{:16}\t"{}"\t{:16}'

    @staticmethod
    def as_text(label):
        """format contents of this item for writing to file"""
        return LabelWriter.field_format.format(str(label.x), str(label.y), label.name, label.anchor_name)


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
                section_text += " {:16}".format(pattern.name)
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


class RuleWriter(SectionWriter):
    """Defines rule-based controls that modify links based on a combination of conditions"""
    SECTION_NAME = "[RULES]"

    @staticmethod
    def as_text(rule):
        """format contents of this item for writing to file"""
        return Rule.SECTION_NAME + '\n' + rule.value


class ControlWriter(SectionWriter):
    """Defines simple controls that modify links based on a single condition"""
    SECTION_NAME = "[CONTROLS]"

    @staticmethod
    def as_text(control):
        """format contents of this item for writing to file"""
        # if control.name:
        #     prefix = " LINK " + control.name + ' ' + control.status
        #     if control.control_type == ControlType.ABOVE or control.control_type == ControlType.BELOW:
        #         return prefix + " IF NODE " + control.node_name + ' ' + control.control_type.name + ' ' + str(control.value)
        #     elif control.control_type == ControlType.TIME and len(control.time) > 0:
        #         return prefix + " AT TIME " + control.time
        #     elif control.control_type == ControlType.CLOCKTIME and len(control.clocktime) > 0:
        #         return prefix + " AT CLOCKTIME " + control.clocktime
        # return ''
        return Control.SECTION_NAME + '\n' + control.value


# class LinkWriter(SectionWriter):
#     """A link in an EPANET model"""
#
#     field_format = "{:16}\t{:16}\t{:16}"
#
#     @staticmethod
#     def as_text(link):
#         """format contents of this item for writing to file"""
#         if len(link.name) > 0:
#             return LinkWriter.field_format.format(link.name, link.inlet_node, link.outlet_node)  # link.description
#         elif link.comment:
#             return link.comment


class PipeWriter():
    """A Pipe link in an EPANET model"""

    field_format = "{:16}\t{:16}\t{:16}\t{:12}\t{:12}\t{:12}\t{:12}\t{:6}\t{}"

    @staticmethod
    def as_text(pipe):
        """format contents of this item for writing to file"""
        if len(pipe.name) > 0:
            return PipeWriter.field_format.format(pipe.name, pipe.inlet_node, pipe.outlet_node, pipe.length, pipe.diameter,
                                            pipe.roughness, pipe.loss_coefficient, pipe.initial_status, pipe.comment)
        elif pipe.comment:
            return pipe.comment


class PumpWriter():
    """A Pump link in an EPANET model"""

    field_format = "{:16}\t{:16}\t{:16}"

    @staticmethod
    def as_text(pump):
        """format contents of this item for writing to file"""
        if len(pump.name) > 0:
            txt = PumpWriter.field_format.format(pump.name, pump.inlet_node, pump.outlet_node)
            if pump.head_curve_name:
                txt += "\tHEAD " + pump.head_curve_name
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


class ValveWriter():
    """A valve link in an EPANET model"""

    field_format = "{:16}\t{:16}\t{:16}\t{:12}\t{:4}\t{:12}\t{:12}\t{}"

    @staticmethod
    def as_text(valve):
        """format contents of this item for writing to file"""
        if len(valve.name) > 0:
            return ValveWriter.field_format.format(valve.name,
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

    field_format = "{:16}\t{}"

    @staticmethod
    def as_text(link):
        """format contents of this item for writing to file"""
        if isinstance(link, Pump) or isinstance(link, Pipe):
            if hasattr(link, "initial_status") and \
               len(link.initial_status) > 0 and \
               link.initial_status.upper() == 'CLOSED':
                return StatusWriter.field_format.format(link.name, link.initial_status)
        elif isinstance(link, Valve):
            if hasattr(link, "initial_status") and \
               len(link.initial_status) > 0 and \
               link.initial_status.upper() != 'ACTIVE':
                return StatusWriter.field_format.format(link.name, link.initial_status)
        #elif status.comment:
        #    return status.comment


class CoordinateWriter(SectionWriter):
    field_format = "{:16}\t{:10}\t{:10}"

    @staticmethod
    def as_text(coordinate):
        """format contents of this item for writing to file"""
        xc, xc_good = ParseData.floatTryParse(coordinate.x)
        yc, yc_good = ParseData.floatTryParse(coordinate.y)
        if not (xc_good and yc_good):
            return ""
        inp = CoordinateWriter.field_format.format(coordinate.name, str(coordinate.x), str(coordinate.y))
        if hasattr(coordinate, "comment") and coordinate.comment:
            inp += "\t"
            if not coordinate.comment.lstrip().startswith(';'):
                inp += "; "
            inp += coordinate.comment
        return inp


class JunctionWriter(SectionWriter):
    """Junction properties"""

    field_format = "{:16}\t{:6}\t{:6}\t{:7}"

    @staticmethod
    def as_text(junction):
        """format contents of this item for writing to file"""
        return JunctionWriter.field_format.format(junction.name, junction.elevation, junction.base_demand_flow, junction.demand_pattern_name)


class ReservoirWriter(SectionWriter):
    """Reservoir properties"""

    field_format = "{:16}\t{:6}\t{:6}\t{}"

    @staticmethod
    def as_text(reservoir):
        """format contents of this item for writing to file"""
        return ReservoirWriter.field_format.format(reservoir.name, reservoir.total_head, reservoir.head_pattern_name, reservoir.comment)


class TankWriter(SectionWriter):
    """Tank properties"""

    field_format = " {:16}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:12}\t{:16}\t{}"

    @staticmethod
    def as_text(tank):
        """format contents of this item for writing to file"""
        return TankWriter.field_format.format(tank.name, tank.elevation, tank.initial_level,
                                        tank.minimum_level, tank.maximum_level, tank.diameter,
                                        tank.minimum_volume, tank.volume_curve, tank.comment)


class MixingWriter(SectionWriter):
    """Mixing model and volume fraction of a Tank"""

    field_format = "{:16}\t{:12}\t{:12}\t{}"

    @staticmethod
    def as_text(tank):
        """format contents of this item for writing to file"""
        mix_model = tank.mixing_model.name.replace("TWO_", "2")
        if mix_model.startswith("2"):
            return MixingWriter.field_format.format(tank.name, mix_model, tank.mixing_fraction,
                                        tank.comment)
        elif mix_model == "FIFO" or mix_model == "LIFO":
            return MixingWriter.field_format.format(tank.name, mix_model, "", tank.comment)
        else:
            # The [MIXING] section is optional.
            # Tanks not described in this section are assumed to be completely mixed.
            return ""


class EmittersWriter(SectionWriter):
    """Emitter coefficients for junctions"""

    field_format = "{:16}\t{:12}\t{}"

    @staticmethod
    def as_text(junction):
        """format contents of this item for writing to file"""
        if len(junction.emitter_coefficient) > 0:
            return EmittersWriter.field_format.format(junction.name,
                                            junction.emitter_coefficient,
                                            junction.comment)
        else:
            return None


class SourceWriter(SectionWriter):
    """Defines locations of water quality sources"""

    field_format = "{:16}\t{:14}\t{:12}\t{}"

    @staticmethod
    def as_text(source):
        inp = ''
        if source.comment:
            inp = source.comment + '\n'
        inp += SourceWriter.field_format.format(source.name,
                                        source.source_type.name,
                                        source.baseline_strength,
                                        source.pattern_name)
        return inp


class DemandWriter(SectionWriter):
    """Define multiple water demands at junction nodes"""

    field_format = "{:16}\t{:9}\t{:10}\t{}"

    @staticmethod
    def as_text(demand):
        inp = ''
        if demand.comment:
            inp = demand.comment + '\n'
        inp += DemandWriter.field_format.format(demand.junction_name,
                                        demand.base_demand,
                                        demand.demand_pattern,
                                        demand.category)
        return inp


class BackdropOptionsWriter(SectionWriter):
    """Identifies a backdrop image and dimensions for the network map"""

    SECTION_NAME = "[BACKDROP]"

    @staticmethod
    def as_text(backdrop_options):
        if backdrop_options:
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

    @staticmethod
    def as_text(energy_options):
        # if energy_options.global_efficiency == "75" \
        #    and energy_options.global_price == "0.0" \
        #    and energy_options.global_pattern == '' \
        #    and energy_options.demand_charge == "0.0" \
        #    and len(energy_options.pumps) == 0:
        #     return ''  # This section has nothing different from defaults, return blank
        # else:
        txt = [SectionWriter.as_text(energy_options)]
        for pump_energy in energy_options.pumps:      # Add text for each pump energy
            txt.append(PumpEnergyWriter.as_text(pump_energy))
        return '\n'.join(txt)


class PumpEnergyWriter(SectionWriter):
    """Parameters used to compute pumping energy and cost for a particular pump"""

    field_format = "PUMP {:16}\t{:8}\t{}\t{}"

    @staticmethod
    def as_text(pump_energy):
        """format contents of this item for writing to file"""
        if len(pump_energy.name) > 0:
            return PumpEnergyWriter.field_format.format(pump_energy.name,
                                            pump_energy.PricePatternEfficiency.name,
                                            pump_energy.value,
                                            pump_energy.comment)
        elif pump_energy.comment:
            return pump_energy.comment


class HydraulicsOptionsWriter(SectionWriter):
    """EPANET Hydraulics Options"""

    SECTION_NAME = "[OPTIONS]"

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
        if hasattr(options, "map") and options.map:
            text_list.append(" MAP                \t" + options.map)
        if options.hydraulics is not None:
            text_list.append(OptionsWriter.section_comments[0])
            text_list.append(HydraulicsOptionsWriter.as_text(options.hydraulics))
        if options.quality is not None:
            text_list.append(OptionsWriter.section_comments[1])
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


class QualityWriter(SectionWriter):
    """Write initial quality to a string"""
    SECTION_NAME = "[QUALITY]"
    field_format = "{:16}\t{}"

    @staticmethod
    def as_text(project):
        text_list = []
        for section in project.nodes_groups():
            for item in section.value:
                if hasattr(item, "initial_quality") and item.initial_quality:
                    name = "Unknown"
                    if hasattr(item, "name") and item.name:
                        name = item.name
                    text_list.append(QualityWriter.field_format.format(name, item.initial_quality))
        if len(text_list) > 0:
            return QualityWriter.SECTION_NAME + '\n' + \
                ";Node           \tInitQuality\n" + \
                ";---------------\t-----------\n" + \
                '\n'.join(text_list)
        else:
            return ''


class ReactionsWriter(SectionWriter):
    """Defines parameters related to chemical reactions occurring in the network"""

    SECTION_NAME = "[REACTIONS]"

    @staticmethod
    def as_text(reactions):
        """format contents of this item for writing to file"""
        #site-specific coefficients first
        txt = ''
        if reactions.value is not None and len(reactions.value) > 0:
            txt = "[REACTIONS]\n"
            txt += ";Type     	Pipe/Tank       	Coefficient\n"
            for loc_spec in reactions.value:
                txt += str(loc_spec) + "\n"
        #global defaults next
        comment_orig = reactions.comment
        if reactions.comment and reactions.comment.lower().startswith(";type"):
            reactions.comment = ""
        txt += "\n" + SectionWriter.as_text(reactions)

        reactions.comment = comment_orig
        # if reactions.comment and reactions.comment.upper().startswith(";TYPE"):
        #     # TODO: implement reactions table as list of reactions
        #     return reactions.value
        # else:
        #     return SectionWriter.as_text(reactions)
        return txt


class ReportOptionsWriter(SectionWriter):
    """Report Options"""

    SECTION_NAME = "[REPORT]"

    @staticmethod
    def as_text(report_options):
        txt = SectionWriter.as_text(report_options)
        try:
            if report_options.nodes:
                txt += '\nNODES ' + ' '.join(report_options.nodes)
            if report_options.links:
                txt += '\nLINKS ' + ' '.join(report_options.links)
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


class TagsWriter(SectionWriter):
    """Write tags to a string"""

    SECTION_NAME = "[TAGS]"

    field_format = "{:10}{:16}\t{:16}"

    @staticmethod
    def as_text(project):
        text_list = [TagsWriter.SECTION_NAME]
        section_map = {"NODE": project.nodes_groups(),
                       "LINK": project.links_groups()}
        for object_type_name, sections in section_map.items():
            for section in sections:
                for item in section.value:
                    if hasattr(item, "tag") and item.tag:
                        name = "Unknown"
                        if hasattr(item, "name") and item.name:
                            name = item.name
                        text_list.append(TagsWriter.field_format.format(object_type_name, item.name, item.tag))
        if len(text_list) > 1:
            return '\n'.join(text_list)
        else:
            return ''
