from core.inp_reader_base import InputFileReader, SectionReaderAsList, SectionReaderAsListGroupByID
from core.epanet.options.times import TimesOptions
from core.epanet.patterns import Pattern
from core.epanet.title import Title
from core.coordinate import Coordinate
from core.epanet.inp_reader_sections import *
from core.epanet.options.hydraulics import flow_units_metric

try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str


class ProjectReader(InputFileReader):
    """Read an EPANET input file into in-memory data structures"""

    def __init__(self):
        """Initialize the sections of an EPANET input file.
           Any sections not initialized here will be handled by the generic core.project_base.Section class."""
        self.read_title = TitleReader()
        self.read_junctions = SectionReaderAsList("[JUNCTIONS]", JunctionReader)
        self.read_reservoirs = SectionReaderAsList("[RESERVOIRS]", ReservoirReader)
        self.read_tanks = SectionReaderAsList("[TANKS]", TankReader)
        self.read_pipes = SectionReaderAsList("[PIPES]", PipeReader)
        self.read_pumps = SectionReaderAsList("[PUMPS]", PumpReader)
        self.read_valves = SectionReaderAsList("[VALVES]", ValveReader)
        self.read_patterns = SectionReaderAsListGroupByID("[PATTERNS]", PatternReader)
        self.read_curves = SectionReaderAsListGroupByID("[CURVES]", CurveReader)
        self.read_energy = EnergyOptionsReader()
        self.read_status = SectionReaderAsList("[STATUS]", StatusReader)
        self.read_controls = ControlReader()
        self.read_rules = RuleReader()
        self.read_demands = SectionReaderAsList("[DEMANDS]", DemandReader)
        self.read_reactions = ReactionsReader()
        self.read_sources = SectionReaderAsList("[SOURCES]", SourceReader)
        # self.read_options = MapOptions,
        self.read_options = OptionsReader()
        self.read_times = TimesOptionsReader()
        self.read_report = ReportOptionsReader()
        self.read_labels = SectionReaderAsList("[LABELS]", LabelReader)
        self.read_backdrop = BackdropOptionsReader()

        # temporary storage for sections that need to be read after other sections
        self.defer_quality = None
        self.defer_coordinates = None
        self.defer_vertices = None
        self.defer_tags = None
        self.defer_mixing = None
        self.defer_emitters = None
        self.defer_status = None
        self.defer_calibrations = None

    def read_section(self, project, section_name, section_text):
        section_name_upper = section_name.upper()
        if section_name_upper == "[QUALITY]":
            self.defer_quality = section_text
            return  # Skip read_section, defer until finished_reading is called.
        elif section_name_upper == "[COORDINATES]":
            self.defer_coordinates = section_text
            return  # Skip read_section, defer until finished_reading is called.
        elif section_name_upper == "[VERTICES]":
            self.defer_vertices = section_text
            return
        elif section_name_upper == "[TAGS]":
            self.defer_tags = section_text
            return  # Skip read_section, defer until finished_reading is called.
        elif section_name_upper == "[MIXING]":
            self.defer_mixing = section_text
            return  # Skip read_section, defer until finished_reading is called.
        elif section_name_upper == "[EMITTERS]":
            self.defer_emitters = section_text
            return  # Skip read_section, defer until finished_reading is called.
        elif section_name_upper == "[STATUS]":
            self.defer_status = section_text
            return
        elif section_name_upper == "[CALIBRATIONS]":
            self.defer_calibrations = section_text
            return
        elif section_name_upper == "[PIPES]":
            # self.check_valid_node_id(project, 'PIPES', section_text)
            pass
        elif section_name_upper == "[PUMPS]":
            # self.check_valid_node_id(project, 'PUMPS', section_text)
            pass
        elif section_name_upper == "[VALVES]":
            # self.check_valid_node_id(project, 'VALVES', section_text)
            pass
        elif section_name_upper == "[DEMANDS]":
            # self.check_valid_node_id(project, 'DEMANDS', section_text)
            pass
        elif section_name_upper == "[SOURCES]":
            # self.check_valid_node_id(project, 'SOURCES', section_text)
            pass
        InputFileReader.read_section(self, project, section_name, section_text)

    def finished_reading(self, project):
        if self.defer_quality:
            # self.check_valid_node_id(project, 'QUALITY', self.defer_quality)
            QualityReader.read(self.defer_quality, project)
            self.defer_quality = None
        if self.defer_coordinates:
            # self.check_valid_node_id(project, 'COORDINATES', self.defer_coordinates)
            CoordinatesReader.read(self.defer_coordinates, project)
            self.defer_coordinates = None
        if self.defer_vertices:
            # self.check_valid_link_id(project, 'VERTICES', self.defer_vertices)
            VerticesReader.read(self.defer_vertices, project)
            self.defer_vertices = None
        if self.defer_tags:
            TagsReader.read(self.defer_tags, project)
            self.defer_tags = None
        if self.defer_mixing:
            # self.check_valid_node_id(project, 'MIXING', self.defer_mixing)
            MixingReader.read(self.defer_mixing, project)
            self.defer_mixing = None
        if self.defer_emitters:
            # self.check_valid_node_id(project, 'EMITTERS', self.defer_emitters)
            EmittersReader.read(self.defer_emitters, project)
            self.defer_emitters = None
        if self.defer_status:
            # self.check_valid_link_id(project, 'STATUS', self.defer_status)
            StatusReader.read(self.defer_status, project)
            self.defer_status = None
        project.metric = project.options.hydraulics.flow_units in flow_units_metric
        project.set_pattern_object_references()


    def check_valid_node_id(self, project, section_name, section_text):
        # check for valid node ids
        temp_text = section_text
        try:
            for line in temp_text.splitlines():
                if line[0:1] == '[' or line[0:1] == ';':
                    pass
                else:
                    fields = line.split()
                    if len(fields) > 0:
                        if "none" in fields[0].lower():
                            pass
                        if section_name == "PIPES" or section_name == "PUMPS" or section_name == "VALVES":
                            node_name = fields[1]
                            found = False
                            for node in project.all_nodes():
                                if node.name == node_name:
                                    found = True
                            if not found:
                                self.input_err_msg += '\n' + 'Undefined Node (' + node_name + ') referenced in ' + section_name + ' section.'
                            node_name = fields[2]
                            found = False
                            for node in project.all_nodes():
                                if node.name == node_name:
                                    found = True
                            if not found:
                                self.input_err_msg += '\n' + 'Undefined Node (' + node_name + ') referenced in ' + section_name + ' section.'
                        elif section_name == "MIXING":
                            node_name = fields[0]
                            found = False
                            for node in project.tanks():
                                if node.name == node_name:
                                    found = True
                            if not found:
                                self.input_err_msg += '\n' + 'Undefined Node (' + node_name + ') referenced in ' + section_name + ' section.'
                        elif section_name == "EMITTERS" or section_name == "DEMANDS":
                            node_name = fields[0]
                            found = False
                            for node in project.junctions():
                                if node.name == node_name:
                                    found = True
                            if not found:
                                self.input_err_msg += '\n' + 'Undefined Node (' + node_name + ') referenced in ' + section_name + ' section.'
                        else:
                            node_name = fields[0]
                            found = False
                            for node in project.all_nodes():
                                if node.name == node_name:
                                    found = True
                            if not found:
                                self.input_err_msg += '\n' + 'Undefined Node (' + node_name + ') referenced in ' + section_name + ' section.'
        except:
            pass


    def check_valid_link_id(self, project, section_name, section_text):
        # check for valid link ids
        temp_text = section_text
        try:
            for line in temp_text.splitlines():
                if line[0:1] == '[' or line[0:1] == ';':
                    pass
                else:
                    fields = line.split()
                    if len(fields) > 0:
                        if "none" in fields[0].lower():
                            pass
                        link_name = fields[0]
                        found = False
                        for link in project.all_links():
                            if link.name == link_name:
                                found = True
                        if not found:
                            self.input_err_msg += '\n' + 'Undefined Link (' + link_name + ') referenced in ' + section_name + ' section.'
        except:
            pass