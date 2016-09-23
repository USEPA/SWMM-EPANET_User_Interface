from core.inp_reader_base import InputFileReader, SectionReaderAsList, SectionReaderAsListGroupByID
from core.epanet.options.times import TimesOptions
from core.epanet.patterns import Pattern
from core.epanet.title import Title
from core.coordinate import Coordinate
from core.epanet.inp_reader_sections import *

try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring


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
        self.read_coordinates = SectionReaderAsList("[COORDINATES]", CoordinateReader)
        self.read_vertices = SectionReaderAsList("[VERTICES]", CoordinateReader)
        self.read_labels = SectionReaderAsList("[LABELS]", LabelReader)
        self.read_backdrop = BackdropOptionsReader()

        # temporary storage for sections that need to be read after other sections
        self.defer_quality = None
        self.defer_coordinates = None
        self.defer_tags = None
        self.defer_mixing = None
        self.defer_emitters = None


    def read_section(self, project, section_name, section_text):
        section_name_upper = section_name.upper()
        if section_name_upper == "[QUALITY]":
            self.defer_quality = section_text
            return  # Skip read_section, defer until finished_reading is called.
        elif section_name_upper == "[COORDINATES]":
            self.defer_coordinates = section_text
            return  # Skip read_section, defer until finished_reading is called.
        elif section_name_upper == "[TAGS]":
            self.defer_tags = section_text
            return  # Skip read_section, defer until finished_reading is called.
        elif section_name_upper == "[MIXING]":
            self.defer_mixing = section_text
            return  # Skip read_section, defer until finished_reading is called.
        elif section_name_upper == "[EMITTERS]":
            self.defer_emitters = section_text
            return  # Skip read_section, defer until finished_reading is called.
        InputFileReader.read_section(self, project, section_name, section_text)


    def finished_reading(self, project):
        if self.defer_quality:
            QualityReader.read(self.defer_quality, project)
            self.defer_quality = None
        if self.defer_coordinates:
            CoordinatesReader.read(self.defer_coordinates, project)
            self.defer_coordinates = None
        if self.defer_tags:
            TagsReader.read(self.defer_tags, project)
            self.defer_tags = None
        if self.defer_mixing:
            MixingReader.read(self.defer_mixing, project)
            self.defer_mixing = None
        if self.defer_emitters:
            EmittersReader.read(self.defer_emitters, project)
