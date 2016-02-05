from core.coordinates import Coordinates
from core.epanet.curves import Curve
from core.epanet.hydraulics.control import Control
from core.epanet.hydraulics.control import Rule
from core.epanet.hydraulics.link import Pipe
from core.epanet.hydraulics.link import Pump
from core.epanet.hydraulics.link import Valve
from core.epanet.hydraulics.node import Demand
from core.epanet.hydraulics.node import Junction
from core.epanet.hydraulics.node import Source
from core.epanet.labels import Label
from core.epanet.options.backdrop import BackdropOptions
from core.epanet.options.energy import EnergyOptions
from core.epanet.options.hydraulics import HydraulicsOptions
from core.epanet.options.map import MapOptions
from core.epanet.options.quality import QualityOptions
from core.epanet.options.reactions import Reactions
from core.epanet.options.report import ReportOptions
from core.epanet.options.times import TimesOptions
from core.epanet.patterns import Pattern
from core.epanet.title import Title
from core.epanet.vertex import Vertex
from core.inputfile import InputFile


class Project(InputFile):
    """Manage a complete EPANET input sequence"""

    # epanet_section_types = {
    #
    #     "[TITLE]": Title,
    #     "[JUNCTIONS]": [Junction],  # junction node information
    #     # [RESERVOIRS]
    #     # [TANKS]
    #     "[PIPES]": [Pipe],
    #     "[PUMPS]": [Pump],
    #     "[VALVES]": [Valve],
    #     "[EMITTERS]": ("[JUNCTIONS]", "emmitter_coefficient"),
    #     "[CURVES]": [Curve],
    #     "[PATTERNS]": [Pattern],   # will this create a collection of them?
    #     "[ENERGY]": EnergyOptions,
    #     # [STATUS]
    #     "[CONTROLS]": [Control],
    #     "[RULES]": [Rule],
    #     "[DEMANDS]": [Demand],
    #     "[QUALITY]": QualityOptions,
    #     "[REACTIONS]": Reactions(Reactions.SECTION_NAME, None, None, -1),
    #     "[SOURCES]": [Source],
    #     # [MIXING]
    #     "[OPTIONS]": MapOptions,
    #     # "[OPTIONS]": EPANETHydraulicsOptions,
    #     "[TIMES]": TimesOptions,
    #     "[REPORT]": ReportOptions,
    #     "[COORDINATES]": [Coordinates],  # X,Y coordinates for nodes
    #     "[VERTICES]": [Vertex],
    #     "[LABELS]": [Label],
    #     "[BACKDROP]": BackdropOptions
    #     # [TAGS]
    #       }

    def __init__(self):
        self.title = Title()
        # self.junctions = [Junction]
        # [RESERVOIRS]
        # [TANKS]
        # self.pipes = [Pipe]
        # self.pumps = [Pump]
        # self.valves = [Valve]
        # self.emitters = [(Junction, "emitter_coefficient")]
        # self.curves = [Curve]
        # self.patterns = [Pattern]
        # self.energy = EnergyOptions()
        # [STATUS]
        # self.controls = [Control]
        # self.rules = [Rule]
        # self.demands = [Demand]
        # self.quality = ReadNodesInitialQuality
        self.options = QualityOptions()
        self.reactions = Reactions()
        self.sources = [Source]
        # [MIXING]
        # self.options = MapOptions,
        self.options = HydraulicsOptions()
        # "[TIMES]": TimesOptions,
        # "[REPORT]": ReportOptions,
        # "[COORDINATES]": [Coordinates],  # X,Y coordinates for nodes
        # "[VERTICES]": [Vertex],
        # "[LABELS]": [Label],
        # "[BACKDROP]": BackdropOptions
        InputFile.__init__(self)
