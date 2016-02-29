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
           Any sections not initialized here will be handled by the generic core.inputfile.Section class.
           Each section is initialized with a """
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
        self.energy = EnergyOptions()
        # [STATUS]
        # self.controls = [Control]
        # self.rules = [Rule]
        # self.demands = [Demand]
        # self.quality = ReadNodesInitialQuality
        self.reactions = Reactions()
        self.sources = [Source]
        # [MIXING]
        # self.options = MapOptions,
        self.options = Options()
        self.times = TimesOptions()
        self.report = ReportOptions()
        # "[COORDINATES]": [Coordinates]  # X,Y coordinates for nodes
        # "[VERTICES]": [Vertex]
        # "[LABELS]": [Label]
        self.backdrop = BackdropOptions()

        InputFile.__init__(self)   # Do this after setting attributes so they will all get added to sections[]
