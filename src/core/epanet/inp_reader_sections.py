import traceback
import shlex
from enum import Enum
from core.project_base import Section, ProjectBase
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
from core.epanet.hydraulics.node import Coordinate
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
from core.epanet.options.times import TimesOptions
from core.inp_reader_base import SectionReader
from core.indexed_list import IndexedList


class CurveReader(SectionReader):
    """Defines a data curve of X,Y points"""

    @staticmethod
    def read(new_text):
        curve = Curve()
        for line in new_text.splitlines():
            comment_split = line.split(';', 1)
            if len(comment_split) == 2:
                # split curve type from description on colon and set
                colon_split = line.split(':', 1)
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
                    curve.name = fields[0]
                    curve.curve_xy.append((fields[1], fields[2]))
        return curve


class LabelReader(SectionReader):
    """A label on the map with location, text, and optional anchor node ID"""

    @staticmethod
    def read(new_text):
        label = Label()
        new_text = SectionReader.set_comment_check_section(label, new_text)
        # fields = shlex.split(new_text.encode('utf8'))
        fields = shlex.split(new_text)
        if len(fields) > 2:
            (label.x, label.y) = fields[0:2]
            # label.name = fields[2].decode('UTF8')
            label.name = fields[2]

            if len(fields) > 3:
                label.anchor_name = fields[3] # name of an anchor node (optional)
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
            comment_split = line.split(';', 1)
            if len(comment_split) == 2:
                pattern.description += line[1:].strip()
                line = comment_split[0].strip()
            if line:
                fields = line.split()
                if len(fields) > 1:
                    pattern.name = fields[0]
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


class RuleReader():
    """Defines rule-based controls that modify links based on a combination of conditions"""
    SECTION_NAME = "[RULES]"

    @staticmethod
    def read(new_text):
        rules = Rule()
        lines = new_text.replace(RuleReader.SECTION_NAME, '').strip().splitlines()
        if len(lines) > 0:
            first_line = lines[0]
            if first_line[0] != ' ':
                lines[0] = ' ' + lines[0]
            rules.value = '\n'.join(lines[0:])
        return rules


class ControlReader():
    """Defines simple controls that modify links based on a single condition"""
    SECTION_NAME = "[CONTROLS]"

    @staticmethod
    def read(new_text):
        controls = Control()
        lines = new_text.replace(ControlReader.SECTION_NAME, '').strip().splitlines()
        if len(lines) > 0:
            first_line = lines[0]
            if first_line[0] != ' ':
                lines[0] = ' ' + lines[0]
            controls.value = '\n'.join(lines[0:])
        return controls

    # @staticmethod
    # def read(new_text):
    #     control = Control()
    #     fields = new_text.split()
    #     control.name, control.status = fields[1], fields[2]
    #     type_str = fields[4].upper()
    #     if type_str == "NODE":
    #         control.node_name = fields[5]
    #         control.control_type = ControlType[fields[6].upper()]
    #         control.value = fields[7]
    #     elif type_str == "TIME":
    #         control.control_type = ControlType.TIME
    #         control.time = fields[5]
    #     elif type_str == "CLOCKTIME":
    #         control.control_type = ControlType.CLOCKTIME
    #         control.clocktime = ' '.join(fields[5:])
    #     else:
    #         raise NameError("Unable to parse Control: " + new_text)
    #     return control


# class LinkReader(SectionReader):
#     """Read a link in an EPANET model"""
#
#     @staticmethod
#     def read(new_text):
#         link = Link()
#         new_text = SectionReader.set_comment_check_section(link, new_text)
#         fields = new_text.split(None, 3)
#         if len(fields) > 2:
#             (link.name, link.inlet_node, link.outlet_node) = fields[0:3]
#             if len(fields) > 3:
#                 link.description = fields[3]
#         return link


class PipeReader():
    """Read a Pipe link in an EPANET model"""

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
            pipe.name, pipe.inlet_node, pipe.outlet_node = fields[0:3]
        if len(fields) > 6:
            pipe.length = fields[3]
            pipe.diameter = fields[4]
            pipe.roughness = fields[5]
            pipe.loss_coefficient = fields[6]
        if len(fields) > 7:
            pipe.initial_status = fields[7]
        return pipe


class PumpReader():
    """Read a Pump link in an EPANET model"""

    @staticmethod
    def read(new_text):
        pump = Pump()
        new_text = SectionReader.set_comment_check_section(pump, new_text)
        fields = new_text.split()
        if len(fields) > 2:
            pump.name, pump.inlet_node, pump.outlet_node = fields[0:3]
            for key_index in range(3, len(fields) - 1, 2):
                value_index = key_index + 1
                if fields[key_index].upper() == "HEAD":
                    pump.head_curve_name = fields[value_index]
                elif fields[key_index].upper() == "POWER":
                    pump.power = fields[value_index]
                elif fields[key_index].upper() == "PATTERN":
                    pump.pattern = fields[value_index]
                elif fields[key_index].upper() == "SPEED":
                    pump.speed = fields[value_index]
        return pump


class ValveReader():
    """Read a valve link in an EPANET model"""

    @staticmethod
    def read(new_text):
        valve = Valve()
        new_text = SectionReader.set_comment_check_section(valve, new_text)
        fields = new_text.split()
        if len(fields) > 2:
            valve.name = fields[0]
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
    def read(new_text, project):
        disposable_section = Section()
        disposable_section.SECTION_NAME = "[STATUS]"
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(disposable_section, line)
            fields = line.split(None)
            if len(fields) > 1:
                link_name = fields[0]
                status = fields[1]
                for link in project.all_links():
                    if link.name == link_name:
                        link.setattr_keep_type("initial_status", status)
                        break


class CoordinateReader(SectionReader):
    @staticmethod
    def read(new_text):
        coordinate = Coordinate()
        fields = new_text.split()
        if len(fields) > 2:
            try:
                coordinate.name = fields[0]
                coordinate.x = float(fields[1])
                coordinate.y = float(fields[2])
                return coordinate
            except:
                print("Problem reading coordinate: " + new_text)
        return None


class CoordinatesReader(SectionReader):
    """Read coordinates of nodes into node objects."""

    @staticmethod
    def read(new_text, project):
        all_nodes = project.all_nodes()
        disposable_section = Section()
        disposable_section.SECTION_NAME = "[COORDINATES]"
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(disposable_section, line)
            coordinate = CoordinateReader.read(line)
            if coordinate:
                try:
                    node = all_nodes[coordinate.name]
                    node.x = coordinate.x
                    node.y = coordinate.y
                except:
                    print("Node not found in model for coordinate " + coordinate.name)


class VerticesReader(SectionReader):
    """Read coordinates of intermediate points of links"""

    @staticmethod
    def read(new_text, project):
        links = project.all_links()
        if links:
            disposable_section = Section()
            disposable_section.SECTION_NAME = "[VERTICES]"
            for line in new_text.splitlines():
                line = SectionReader.set_comment_check_section(disposable_section, line)
                coordinate = CoordinateReader.read(line)
                if coordinate:
                    try:
                        link = links[coordinate.name]
                        link.vertices.append(coordinate)
                    except Exception:
                        print("Link not found in model for vertex " + coordinate.name)


class QualityReader(SectionReader):
    """Read initial water quality at each node into project."""

    @staticmethod
    def read(new_text, project):
        disposable_section = Section()
        disposable_section.SECTION_NAME = "[QUALITY]"
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(disposable_section, line)
            fields = line.split(None, 1)
            if len(fields) > 1:
                node_name = fields[0]
                initial_quality = fields[1]
                for nodes in (project.junctions.value, project.reservoirs.value, project.tanks.value):
                    for node in nodes:
                        if node.name == node_name:
                            node.setattr_keep_type("initial_quality", initial_quality)
                            break


class JunctionReader(SectionReader):
    """Junction properties"""

    @staticmethod
    def read(new_text):
        junction = Junction()
        new_text = SectionReader.set_comment_check_section(junction, new_text)
        fields = new_text.split()
        if len(fields) > 0:
            junction.name = fields[0]
        if len(fields) > 1:
            junction.elevation = fields[1]
        if len(fields) > 2:
            junction.base_demand_flow = fields[2]
        if len(fields) > 3:
            junction.demand_pattern_name = fields[3]
        return junction


class ReservoirReader(SectionReader):
    """Reservoir properties"""

    @staticmethod
    def read(new_text):
        reservoir = Reservoir()
        new_text = SectionReader.set_comment_check_section(reservoir, new_text)
        fields = new_text.split()
        if len(fields) > 0:
            reservoir.name = fields[0]
        if len(fields) > 1:
            reservoir.total_head = fields[1]
        if len(fields) > 2:
            reservoir.head_pattern_name = fields[2]
        return reservoir


class TankReader(SectionReader):
    """Tank properties"""

    @staticmethod
    def read(new_text):
        tank = Tank()
        new_text = SectionReader.set_comment_check_section(tank, new_text)
        fields = new_text.split()
        if len(fields) > 0:
            tank.name = fields[0]
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
    def read(new_text, project):
        disposable_section = Section()
        disposable_section.SECTION_NAME = "[MIXING]"
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(disposable_section, line)
            fields = line.split(None)
            if len(fields) > 1:
                node_name = fields[0]
                mixing_model = MixingModel[fields[1].upper().replace("2", "TWO_")]
                if len(fields) > 2:
                    mixing_fraction = fields[2]
                for tank in (project.tanks.value):
                    if tank.name == node_name:
                        tank.setattr_keep_type("mixing_model", mixing_model)
                        if len(fields) > 2:
                            tank.setattr_keep_type("mixing_fraction", mixing_fraction)
                    break


class EmittersReader(SectionReader):
    """Emitters and associated coefficient for junctions"""

    @staticmethod
    def read(new_text, project):
        disposable_section = Section()
        disposable_section.SECTION_NAME = "[EMITTERS]"
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(disposable_section, line)
            fields = line.split(None)
            if len(fields) > 1:
                node_name = fields[0]
                emitter_coefficient = fields[1]
                for node in project.junctions.value:
                    if node.name == node_name:
                        node.setattr_keep_type("emitter_coefficient", emitter_coefficient)
                        break


class SourceReader(SectionReader):
    """Defines locations of water quality sources"""


    @staticmethod
    def read(new_text):
        source = Source()
        fields = new_text.split()
        if len(fields) > 0:
            source.name = fields[0]
        if len(fields) > 1:
            source.source_type = SourceType[fields[1].upper()]
        if len(fields) > 2:
            source.baseline_strength = fields[2]
        if len(fields) > 3:
            source.pattern_name = fields[3]
        return source


class DemandReader(SectionReader):
    """Define multiple water demands at junction nodes"""


    @staticmethod
    def read(new_text):
        demand = Demand()
        fields = new_text.split()
        if len(fields) > 0:
            demand.junction_name = fields[0]
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
                        backdrop_options.setattr_keep_type(ProjectBase.format_as_attribute_name(fields[0]), fields[1])
            except:
                print("BackdropOptions skipping input line: " + line)
        return backdrop_options


class EnergyOptionsReader(SectionReader):
    """Defines global parameters used to compute pumping energy and cost"""

    SECTION_NAME = "[ENERGY]"

    @staticmethod
    def read(new_text):
        energy_options = EnergyOptions()
        for line in new_text.splitlines():
            try:
                line = SectionReader.set_comment_check_section(energy_options, line)
                fields = line.split()
                if len(fields) > 1:
                    if fields[0].upper() == "PUMP":
                        energy_options.pumps.append(PumpEnergyReader.read(line))
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
            pump_energy.name = fields[1]
            pump_energy.PricePatternEfficiency = PumpEnergyType[fields[2].upper()]
            pump_energy.value = fields[3]
        return pump_energy


class HydraulicsOptionsReader(SectionReader):
    """EPANET Hydraulics Options"""

    SECTION_NAME = "[OPTIONS]"

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
        for comment in OptionsReader.section_comments:
            new_text = new_text.replace(comment + '\n', '')
        options.hydraulics = HydraulicsOptionsReader.read(new_text)
        options.quality = QualityOptionsReader.read(new_text)
        for line in new_text.splitlines():
            line_list = line.split()
            if line_list:
                if str(line_list[0]).strip().upper() == "MAP":
                    options.map = ' '.join(line_list[1:])
        return options


class TimesOptionsReader(SectionReader):
    """Read model duration, time step, etc."""

    SECTION_NAME = "[TIMES]"

    @staticmethod
    def read(new_text):
        times_options = TimesOptions()
        for line in new_text.splitlines():
            try:
                SectionReader.set_text_line(times_options, line)
            except:
                print("TimesOptionsReader skipping input line: " + line)
        return times_options


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
                reactions.value.append(upper_line)
                #reactions.comment += '\n' + line  # TODO: parse into table of per pipe values
            else:
                SectionReader.set_text_line(reactions, line)
        return reactions


class ReportOptionsReader(SectionReader):
    """Report Options"""

    SECTION_NAME = "[REPORT]"
    section_type = ReportOptions

    @staticmethod
    def read(new_text):
        """Read this section from the text representation"""
        report_options = ReportOptions()
        lines = new_text.splitlines()
        for line in lines:
            line = SectionReader.set_comment_check_section(report_options, line)
            if line:
                (attr_name, attr_value) = line.split(None, 1)
                attr_name = attr_name.upper()
                if attr_name == "NODES":
                    report_options.nodes.extend(attr_value.split())
                elif attr_name == "LINKS":
                    report_options.links.extend(attr_value.split())
                elif attr_name == "STATUS":
                    report_options.setattr_keep_type("status", attr_value)
                elif attr_name == "FILE":
                    report_options.file = attr_value
                elif attr_name == "SUMMARY":
                    report_options.setattr_keep_type("summary", attr_value)
                elif attr_name == "PAGESIZE" or attr_name == "PAGE":
                    report_options.pagesize = attr_value
                elif attr_name == "ENERGY":
                    report_options.setattr_keep_type("energy", attr_value)
                else:
                    report_options.parameters.append(line)
        return report_options

    # @staticmethod
    # def read(new_text):
    #     """Set this section from text.
    #         Args:
    #             line (str): One line of text formatted as input file.
    #     """
    #     report_options = ReportOptions()
    #     for line in new_text.splitlines():
    #         line = SectionReader.set_comment_check_section(report_options, line)
    #         if line.strip():
    #             # Set fields from metadata
    #             (attr_name, attr_value) = SectionReader.get_attr_name_value(report_options, line)
    #             if attr_name:  # Set fields from metadata
    #                 try:
    #                     report_options.setattr_keep_type(attr_name, attr_value)
    #                     #xw09/13/2016 return
    #                 except:
    #                     print("Section report could not set " + attr_name)
    #             else:
    #                 report_options.parameters.append(line)
    #     return report_options


class TagsReader(SectionReader):
    """Read tag information from text into project objects that have tags"""

    @staticmethod
    def read(new_text, project):
        section_map = {"NODE": project.nodes_groups(),
                       "LINK": project.links_groups()}
        disposable_tags = Section()
        disposable_tags.SECTION_NAME = "[TAGS]"
        for line in new_text.splitlines():
            line = SectionReader.set_comment_check_section(disposable_tags, line)
            fields = line.split()
            if len(fields) > 2:
                object_type_name = fields[0].upper()
                object_name = fields[1].upper()
                tag = ' '.join(fields[2:])
                sections = section_map[object_type_name]
                found = False
                for section in sections:
                    for candidate in section.value:
                        if candidate.name.upper() == object_name:
                            candidate.tag = tag
                            found = True
                            # print ("Tagged: " + type(candidate).__name__ + ' ' + candidate.name + ' = ' + tag)
                            break
                    if found:
                        break
                if not found:
                    print ("Tag not applied: " + line + "\n")
