from core.inputfile import SectionAsListOf, SectionAsListGroupByID
from core.epanet.curves import Curve
from core.epanet.hydraulics.control import Control
from core.epanet.hydraulics.link import Pipe
from core.epanet.hydraulics.link import Pump
from core.epanet.hydraulics.link import Valve
from core.epanet.hydraulics.node import Coordinate
from core.epanet.hydraulics.node import Demand
from core.epanet.hydraulics.node import Quality
from core.epanet.hydraulics.node import Junction
from core.epanet.hydraulics.node import Reservoir
from core.epanet.hydraulics.node import Tank, Mixing
from core.epanet.hydraulics.node import Source
from core.epanet.labels import Label
from core.epanet.options.options import Options
from core.epanet.options.backdrop import BackdropOptions
from core.epanet.options.energy import EnergyOptions
from core.epanet.options.reactions import Reactions
from core.epanet.options.report import ReportOptions
from core.epanet.options.times import TimesOptions
from core.epanet.patterns import Pattern
from core.epanet.title import Title
from core.epanet.vertex import Vertex
from core.inputfile import InputFile


class Project(InputFile):
    """Manage a complete EPANET input sequence"""

    def __init__(self):
        """Initialize the sections of an EPANET input file.
           Any sections not initialized here will be handled by the generic core.inputfile.Section class."""
        self.title = Title()
        self.junctions = SectionAsListOf("[JUNCTIONS]", Junction,
                                         ";ID             \tElev  \tDemand\tPattern\n"
                                         ";---------------\t------\t------\t-------")
        self.reservoirs = SectionAsListOf("[RESERVOIRS]", Reservoir,
                                          ";ID             \tHead        \tPattern\n"
                                          ";---------------\t------------\t-------")
        self.tanks = SectionAsListOf("[TANKS]", Tank,
            ";ID              \tElevation   \tInitLevel   \tMinLevel    \tMaxLevel    \tDiameter    \tMinVol      \tVolCurve")

        self.mixing = SectionAsListOf("[MIXING]", Mixing, ";Tank           \tModel       \tMixing Volume Fraction\n"
                                                          ";---------------\t------------\t----------------------")
        self.pipes = SectionAsListOf("[PIPES]", Pipe, ";ID             \tNode1           \tNode2           \t"
                                     "Length      \tDiameter    \tRoughness   \tMinorLoss   \tStatus")
        self.pumps = SectionAsListOf("[PUMPS]", Pump,
                                     ";ID             \tNode1           \tNode2           \tParameters")
        self.valves = SectionAsListOf("[VALVES]", Valve,
            ";ID              \tNode1           \tNode2           \tDiameter    \tType\tSetting     \tMinorLoss   ")
        # self.emitters = [(Junction, "emitter_coefficient")]
        self.patterns = SectionAsListGroupByID("[PATTERNS]", Pattern,
                                               ";ID              \tMultipliers\n"
                                               ";----------------\t-----------")
        self.curves = SectionAsListGroupByID("[CURVES]", Curve,
                                             ";ID              \tX-Value     \tY-Value\n"
                                             ";----------------\t------------\t-------")
        self.energy = EnergyOptions()
        # [STATUS]
        self.controls = SectionAsListOf("[CONTROLS]", Control)
        self.rules = SectionAsListOf("[RULES]", basestring)
        self.demands = SectionAsListOf("[DEMANDS]", Demand,
                                       ";ID             \tDemand   \tPattern   \tCategory\n"
                                       ";---------------\t---------\t----------\t--------")

        self.quality = SectionAsListOf("[QUALITY]", Quality,
                                       ";Node           \tInitQuality\n"
                                       ";---------------\t-----------")
        self.reactions = Reactions()
        self.sources = SectionAsListOf("[SOURCES]", Source,
                                       ";Node           \tType          \tStrength    \tPattern\n"
                                       ";---------------\t--------------\t------------\t-------")
        # [MIXING]
        # self.options = MapOptions,
        self.options = Options()
        self.times = TimesOptions()
        self.report = ReportOptions()
        self.coordinates = SectionAsListOf("[COORDINATES]", Coordinate, ";Node            \tX-Coord         \tY-Coord")
        # "[VERTICES]": [Vertex]
        self.labels = SectionAsListOf("[LABELS]", Label, ";X-Coord        \tY-Coord         \tLabel & Anchor Node")
        self.backdrop = BackdropOptions()

        InputFile.__init__(self)   # Do this after setting attributes so they will all get added to sections[]
