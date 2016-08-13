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
        self.read_mixing = SectionReaderAsList("[MIXING]", MixingReader)
        self.read_pipes = SectionReaderAsList("[PIPES]", PipeReader)
        self.read_pumps = SectionReaderAsList("[PUMPS]", PumpReader)
        self.read_valves = SectionReaderAsList("[VALVES]", ValveReader)
        # self.read_emitters = [(Junction, "emitter_coefficient")]
        self.read_patterns = SectionReaderAsListGroupByID("[PATTERNS]", PatternReader)
        self.read_curves = SectionReaderAsListGroupByID("[CURVES]", CurveReader)
        self.read_energy = EnergyOptionsReader()
        self.read_status = SectionReaderAsList("[STATUS]", StatusReader)
        self.read_controls = SectionReaderAsList("[CONTROLS]", ControlReader)
        self.read_rules = SectionReaderAsList("[RULES]", SectionReader)
        self.read_demands = SectionReaderAsList("[DEMANDS]", DemandReader)

        self.read_quality = SectionReaderAsList("[QUALITY]", QualityReader)
        self.read_reactions = ReactionsReader()
        self.read_sources = SectionReaderAsList("[SOURCES]", SourceReader)
        # [MIXING]
        # self.read_options = MapOptions,
        self.read_options = OptionsReader()
        # self.read_times = TimesOptionsReader()
        self.read_report = ReportOptionsReader()
        self.read_coordinates = SectionReaderAsList("[COORDINATES]", CoordinateReader)
        self.read_coordinates = SectionReaderAsList("[VERTICES]", CoordinateReader)
        self.read_labels = SectionReaderAsList("[LABELS]", LabelReader)
        self.read_backdrop = BackdropOptionsReader()
