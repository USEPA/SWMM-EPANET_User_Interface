from core.inp_reader_base import InputFileReader, SectionReaderAsListOf, SectionReaderAsListGroupByID
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
        self.read_junctions = SectionReaderAsListOf("[JUNCTIONS]", Junction, JunctionReader,
                                                    ";ID             \tElev  \tDemand\tPattern\n"
                                                    ";---------------\t------\t------\t-------")
        self.read_reservoirs = SectionReaderAsListOf("[RESERVOIRS]", Reservoir, ReservoirReader,
                                                     ";ID             \tHead        \tPattern\n"
                                                     ";---------------\t------------\t-------")
        self.read_tanks = SectionReaderAsListOf("[TANKS]", Tank, TankReader,
            ";ID              \tElevation   \tInitLevel   \tMinLevel    \tMaxLevel    \tDiameter    \tMinVol      \tVolCurve")

        self.read_mixing = SectionReaderAsListOf("[MIXING]", Mixing, MixingReader,
                                                 ";Tank           \tModel       \tMixing Volume Fraction\n"
                                                 ";---------------\t------------\t----------------------")
        self.read_pipes = SectionReaderAsListOf("[PIPES]", Pipe, PipeReader,
                                                ";ID             \tNode1           \tNode2           \t"
                                                "Length      \tDiameter    \tRoughness   \tMinorLoss   \tStatus")
        self.read_pumps = SectionReaderAsListOf("[PUMPS]", Pump, PumpReader,
                                                ";ID             \tNode1           \tNode2           \tParameters")
        self.read_valves = SectionReaderAsListOf("[VALVES]", Valve, ValveReader,
            ";ID              \tNode1           \tNode2           \tDiameter    \tType\tSetting     \tMinorLoss   ")
        # self.read_emitters = [(Junction, "emitter_coefficient")]
        self.read_patterns = SectionReaderAsListGroupByID("[PATTERNS]", Pattern, PatternReader,
                                                          ";ID              \tMultipliers\n"
                                                          ";----------------\t-----------")
        self.read_curves = SectionReaderAsListGroupByID("[CURVES]", Curve, CurveReader,
                                                        ";ID              \tX-Value     \tY-Value\n"
                                                        ";----------------\t------------\t-------")
        self.read_energy = EnergyOptionsReader()
        self.read_status = SectionReaderAsListOf("[STATUS]", Status, StatusReader, ";ID             \tStatus/Setting")
        self.read_controls = SectionReaderAsListOf("[CONTROLS]", Control, ControlReader, None)
        self.read_rules = SectionReaderAsListOf("[RULES]", basestring, SectionReader, None)
        self.read_demands = SectionReaderAsListOf("[DEMANDS]", Demand, DemandReader,
                                                  ";ID             \tDemand   \tPattern   \tCategory\n"
                                                  ";---------------\t---------\t----------\t--------")

        self.read_quality = SectionReaderAsListOf("[QUALITY]", Quality, QualityReader,
                                                  ";Node           \tInitQuality\n"
                                                  ";---------------\t-----------")
        self.read_reactions = ReactionsReader()
        self.read_sources = SectionReaderAsListOf("[SOURCES]", Source, SourceReader,
                                                  ";Node           \tType          \tStrength    \tPattern\n"
                                                  ";---------------\t--------------\t------------\t-------")
        # [MIXING]
        # self.read_options = MapOptions,
        self.read_options = OptionsReader()
        # self.read_times = TimesOptionsReader()
        self.read_report = ReportOptionsReader()
        self.read_coordinates = SectionReaderAsListOf("[COORDINATES]", Coordinate, CoordinateReader,
                                                      ";Node            \tX-Coord         \tY-Coord")
        # X,Y coordinates for nodes

        # "[VERTICES]": [Vertex]
        self.read_labels = SectionReaderAsListOf("[LABELS]", Label, LabelReader,
                                                 ";X-Coord        \tY-Coord         \tLabel & Anchor Node")
        self.read_backdrop = BackdropOptionsReader()
