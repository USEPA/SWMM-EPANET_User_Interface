from core.project_base import Project, Section, SectionAsListOf
from core.epanet.curves import Curve
from core.epanet.hydraulics.control import Control
from core.epanet.hydraulics.link import Pipe
from core.epanet.hydraulics.link import Pump
from core.epanet.hydraulics.link import Valve
from core.epanet.hydraulics.link import Status
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


class EpanetProject(Project):
    """Manage a complete EPANET input sequence"""

    def __init__(self):
        """Initialize the sections of an EPANET input file.
           Any sections not initialized here will be handled by the generic core.project_base.Section class."""
        self.title = Title()
        self.junctions = SectionAsListOf("[JUNCTIONS]", Junction)
        self.reservoirs = SectionAsListOf("[RESERVOIRS]", Reservoir)
        self.tanks = SectionAsListOf("[TANKS]", Tank)

        self.mixing = SectionAsListOf("[MIXING]", Mixing)
        self.pipes = SectionAsListOf("[PIPES]", Pipe)
        self.pumps = SectionAsListOf("[PUMPS]", Pump)
        self.valves = SectionAsListOf("[VALVES]", Valve)
        # self.emitters = [(Junction, "emitter_coefficient")]
        self.patterns = SectionAsListOf("[PATTERNS]", Pattern)
        self.curves = SectionAsListOf("[CURVES]", Curve)
        self.energy = EnergyOptions()
        self.status = SectionAsListOf("[STATUS]", Status)
        self.controls = SectionAsListOf("[CONTROLS]", Control)
        self.rules = SectionAsListOf("[RULES]", basestring)
        self.demands = SectionAsListOf("[DEMANDS]", Demand)

        self.quality = SectionAsListOf("[QUALITY]", Quality)
        self.reactions = Reactions()
        self.sources = SectionAsListOf("[SOURCES]", Source)
        # [MIXING]
        # self.options = MapOptions,
        self.options = Options()
        self.times = TimesOptions()
        self.report = ReportOptions()
        self.coordinates = SectionAsListOf("[COORDINATES]", Coordinate)
        # "[VERTICES]": [Vertex]
        self.labels = SectionAsListOf("[LABELS]", Label)
        self.backdrop = BackdropOptions()

        Project.__init__(self)   # Do this after setting attributes so they will all get added to sections[]
