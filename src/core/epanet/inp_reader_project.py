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
        self.read_junctions = SectionReaderAsList("[JUNCTIONS]", JunctionReader,
                                                    ";ID             \tElev  \tDemand\tPattern\n"
                                                    ";---------------\t------\t------\t-------")
        self.read_reservoirs = SectionReaderAsList("[RESERVOIRS]", ReservoirReader,
                                                     ";ID             \tHead        \tPattern\n"
                                                     ";---------------\t------------\t-------")
        self.read_tanks = SectionReaderAsList("[TANKS]", TankReader,
            ";ID              \tElevation   \tInitLevel   \tMinLevel    \tMaxLevel    \tDiameter    \tMinVol      \tVolCurve")

        self.read_mixing = SectionReaderAsList("[MIXING]", MixingReader,
                                                 ";Tank           \tModel       \tMixing Volume Fraction\n"
                                                 ";---------------\t------------\t----------------------")
        self.read_pipes = SectionReaderAsList("[PIPES]", PipeReader,
                                                ";ID             \tNode1           \tNode2           \t"
                                                "Length      \tDiameter    \tRoughness   \tMinorLoss   \tStatus")
        self.read_pumps = SectionReaderAsList("[PUMPS]", PumpReader,
                                                ";ID             \tNode1           \tNode2           \tParameters")
        self.read_valves = SectionReaderAsList("[VALVES]", ValveReader,
            ";ID              \tNode1           \tNode2           \tDiameter    \tType\tSetting     \tMinorLoss   ")
        # self.read_emitters = [(Junction, "emitter_coefficient")]
        self.read_patterns = SectionReaderAsListGroupByID("[PATTERNS]", PatternReader,
                                                          ";ID              \tMultipliers\n"
                                                          ";----------------\t-----------")
        self.read_curves = SectionReaderAsListGroupByID("[CURVES]", CurveReader,
                                                        ";ID              \tX-Value     \tY-Value\n"
                                                        ";----------------\t------------\t-------")
        self.read_energy = EnergyOptionsReader()
        self.read_status = SectionReaderAsList("[STATUS]", StatusReader, ";ID             \tStatus/Setting")
        self.read_controls = SectionReaderAsList("[CONTROLS]", ControlReader, None)
        self.read_rules = SectionReaderAsList("[RULES]", SectionReader, None)
        self.read_demands = SectionReaderAsList("[DEMANDS]", DemandReader,
                                                  ";ID             \tDemand   \tPattern   \tCategory\n"
                                                  ";---------------\t---------\t----------\t--------")

        self.read_quality = SectionReaderAsList("[QUALITY]", QualityReader,
                                                  ";Node           \tInitQuality\n"
                                                  ";---------------\t-----------")
        self.read_reactions = ReactionsReader()
        self.read_sources = SectionReaderAsList("[SOURCES]", SourceReader,
                                                  ";Node           \tType          \tStrength    \tPattern\n"
                                                  ";---------------\t--------------\t------------\t-------")
        # [MIXING]
        # self.read_options = MapOptions,
        self.read_options = OptionsReader()
        # self.read_times = TimesOptionsReader()
        self.read_report = ReportOptionsReader()
        self.read_coordinates = SectionReaderAsList("[COORDINATES]", CoordinateReader,
                                                      ";Node            \tX-Coord         \tY-Coord")
        # X,Y coordinates for nodes

        # "[VERTICES]": [Vertex]
        self.read_labels = SectionReaderAsList("[LABELS]", LabelReader,
                                                 ";X-Coord        \tY-Coord         \tLabel & Anchor Node")
        self.read_backdrop = BackdropOptionsReader()
