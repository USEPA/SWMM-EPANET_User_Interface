from core.inp_writer_base import InputFileWriterBase, SectionWriterAsList
from core.epanet.options.times import TimesOptions
from core.epanet.patterns import Pattern
from core.epanet.title import Title
from core.epanet.vertex import Vertex

from core.epanet.inp_writer_sections import *

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


class ProjectWriter(InputFileWriterBase):
    """Read an EPANET input file into in-memory data structures"""

    def __init__(self):
        """Initialize the sections of an EPANET input file.
           Any sections not initialized here will be handled by the generic core.project_base.Section class."""
        self.write_title = TitleWriter()
        self.write_junctions = SectionWriterAsList("[JUNCTIONS]", JunctionWriter,
                                                   ";ID             \tElev  \tDemand\tPattern\n"
                                                   ";---------------\t------\t------\t-------")
        self.write_reservoirs = SectionWriterAsList("[RESERVOIRS]", ReservoirWriter,
                                                    ";ID             \tHead        \tPattern\n"
                                                    ";---------------\t------------\t-------")
        self.write_tanks = SectionWriterAsList("[TANKS]", TankWriter,
            ";ID              \tElevation   \tInitLevel   \tMinLevel    \tMaxLevel    \tDiameter    \tMinVol      \tVolCurve")

        self.write_mixing = SectionWriterAsList("[MIXING]", MixingWriter,
                                                ";Tank           \tModel       \tMixing Volume Fraction\n"
                                                ";---------------\t------------\t----------------------")
        self.write_pipes = SectionWriterAsList("[PIPES]", PipeWriter,
                                               ";ID             \tNode1           \tNode2           \t"
                                                 "Length      \tDiameter    \tRoughness   \tMinorLoss   \tStatus")
        self.write_pumps = SectionWriterAsList("[PUMPS]", PumpWriter,
                                               ";ID             \tNode1           \tNode2           \tParameters")
        self.write_valves = SectionWriterAsList("[VALVES]", ValveWriter,
            ";ID              \tNode1           \tNode2           \tDiameter    \tType\tSetting     \tMinorLoss   ")
        # self.write_emitters = [(Junction, "emitter_coefficient")]
        self.write_patterns = SectionWriterAsList("[PATTERNS]", PatternWriter,
                                                  ";ID              \tMultipliers\n"
                                                  ";----------------\t-----------")
        self.write_curves = SectionWriterAsList("[CURVES]", CurveWriter,
                                                ";ID              \tX-Value     \tY-Value\n"
                                                ";----------------\t------------\t-------")
        self.write_energy = EnergyOptionsWriter()
        self.write_status = SectionWriterAsList("[STATUS]", StatusWriter, ";ID             \tStatus/Setting")
        self.write_controls = SectionWriterAsList("[CONTROLS]", ControlWriter, None)
        self.write_rules = SectionWriterAsList("[RULES]", SectionWriter, None)
        self.write_demands = SectionWriterAsList("[DEMANDS]", DemandWriter,
                                                 ";ID             \tDemand   \tPattern   \tCategory\n"
                                                 ";---------------\t---------\t----------\t--------")

        self.write_quality = SectionWriterAsList("[QUALITY]", QualityWriter,
                                                 ";Node           \tInitQuality\n"
                                                 ";---------------\t-----------")
        self.write_reactions = ReactionsWriter()
        self.write_sources = SectionWriterAsList("[SOURCES]", SourceWriter,
                                                 ";Node           \tType          \tStrength    \tPattern\n"
                                                 ";---------------\t--------------\t------------\t-------")
        # [MIXING]
        self.write_options = OptionsWriter()
        self.write_times = SectionWriter()
        self.write_report = ReportOptionsWriter()
        self.write_coordinates = SectionWriterAsList("[COORDINATES]", CoordinateWriter,
                                                     ";Node            \tX-Coord   \tY-Coord")
        self.write_vertices = SectionWriterAsList("[VERTICES]", CoordinateWriter,
                                                  ";Link            \tX-Coord   \tY-Coord")
        self.write_labels = SectionWriterAsList("[LABELS]", LabelWriter,
                                                ";X-Coord        \tY-Coord         \tLabel & Anchor Node")
        self.write_backdrop = BackdropOptionsWriter()
