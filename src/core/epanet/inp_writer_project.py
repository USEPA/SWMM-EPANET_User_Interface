from core.inp_writer_base import InputFileWriterBase, SectionWriterAsListOf
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
        self.write_junctions = SectionWriterAsListOf("[JUNCTIONS]", Junction, JunctionWriter,
                                                     ";ID             \tElev  \tDemand\tPattern\n"
                                                     ";---------------\t------\t------\t-------")
        self.write_reservoirs = SectionWriterAsListOf("[RESERVOIRS]", Reservoir, ReservoirWriter,
                                                      ";ID             \tHead        \tPattern\n"
                                                      ";---------------\t------------\t-------")
        self.write_tanks = SectionWriterAsListOf("[TANKS]", Tank, TankWriter,
            ";ID              \tElevation   \tInitLevel   \tMinLevel    \tMaxLevel    \tDiameter    \tMinVol      \tVolCurve")

        self.write_mixing = SectionWriterAsListOf("[MIXING]", Mixing, MixingWriter,
                                                  ";Tank           \tModel       \tMixing Volume Fraction\n"
                                                  ";---------------\t------------\t----------------------")
        self.write_pipes = SectionWriterAsListOf("[PIPES]", Pipe, PipeWriter,
                                                 ";ID             \tNode1           \tNode2           \t"
                                                 "Length      \tDiameter    \tRoughness   \tMinorLoss   \tStatus")
        self.write_pumps = SectionWriterAsListOf("[PUMPS]", Pump, PumpWriter,
                                                 ";ID             \tNode1           \tNode2           \tParameters")
        self.write_valves = SectionWriterAsListOf("[VALVES]", Valve, ValveWriter,
            ";ID              \tNode1           \tNode2           \tDiameter    \tType\tSetting     \tMinorLoss   ")
        # self.write_emitters = [(Junction, "emitter_coefficient")]
        self.write_patterns = SectionWriterAsListOf("[PATTERNS]", Pattern, PatternWriter,
                                                    ";ID              \tMultipliers\n"
                                                    ";----------------\t-----------")
        self.write_curves = SectionWriterAsListOf("[CURVES]", Curve, CurveWriter,
                                                  ";ID              \tX-Value     \tY-Value\n"
                                                  ";----------------\t------------\t-------")
        self.write_energy = EnergyOptionsWriter()
        self.write_status = SectionWriterAsListOf("[STATUS]", Status, StatusWriter, ";ID             \tStatus/Setting")
        self.write_controls = SectionWriterAsListOf("[CONTROLS]", Control, ControlWriter, None)
        self.write_rules = SectionWriterAsListOf("[RULES]", basestring, SectionWriter, None)
        self.write_demands = SectionWriterAsListOf("[DEMANDS]", Demand, DemandWriter,
                                                   ";ID             \tDemand   \tPattern   \tCategory\n"
                                                   ";---------------\t---------\t----------\t--------")

        self.write_quality = SectionWriterAsListOf("[QUALITY]", Quality, QualityWriter,
                                                   ";Node           \tInitQuality\n"
                                                   ";---------------\t-----------")
        self.write_reactions = ReactionsWriter()
        self.write_sources = SectionWriterAsListOf("[SOURCES]", Source, SourceWriter,
                                                   ";Node           \tType          \tStrength    \tPattern\n"
                                                   ";---------------\t--------------\t------------\t-------")
        # [MIXING]
        # self.write_options = MapOptions,
        self.write_options = OptionsWriter()
        # self.write_times = TimesOptionsWriter()
        self.write_report = ReportOptionsWriter()
        self.write_coordinates = SectionWriterAsListOf("[COORDINATES]", Coordinate, CoordinateWriter,
                                                       ";Node            \tX-Coord         \tY-Coord")
        # "[VERTICES]": [Vertex]
        self.write_labels = SectionWriterAsListOf("[LABELS]", Label, LabelWriter,
                                                  ";X-Coord        \tY-Coord         \tLabel & Anchor Node")
        self.write_backdrop = BackdropOptionsWriter()
