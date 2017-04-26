from core.project_base import ProjectBase, Section, SectionAsList
from core.epanet.curves import Curve
from core.epanet.hydraulics.control import Control
from core.epanet.hydraulics.control import Rule
from core.epanet.hydraulics.link import Pipe
from core.epanet.hydraulics.link import Pump
from core.epanet.hydraulics.link import Valve
from core.epanet.hydraulics.link import Status
from core.epanet.hydraulics.node import Coordinate
from core.epanet.hydraulics.node import Demand
from core.epanet.hydraulics.node import Junction
from core.epanet.hydraulics.node import Reservoir
from core.epanet.hydraulics.node import Tank
from core.epanet.hydraulics.node import Source
from core.epanet.labels import Label
from core.epanet.options.options import Options
from core.epanet.options.backdrop import BackdropOptions
from core.swmm.options.map import MapOptions
from core.epanet.options.energy import EnergyOptions
from core.epanet.options.reactions import Reactions
from core.epanet.options.report import ReportOptions
from core.epanet.options.times import TimesOptions
from core.epanet.patterns import Pattern
from core.epanet.title import Title
from core.epanet.vertex import Vertex
import core.epanet.calibration as Cali
from core.indexed_list import IndexedList

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


class EpanetProject(ProjectBase):
    """Manage a complete EPANET input sequence"""

    def __init__(self):
        """Initialize the sections of an EPANET input file.
           Any sections not initialized here will be handled by the generic core.project_base.Section class."""
        ProjectBase.__init__(self)

        self.title = Title()
        self.backdrop = BackdropOptions()       # BACKDROP      bounding rectangle and file name of backdrop image
        self.map = MapOptions()                 # MAP           map's bounding rectangle and units
        self.junctions = SectionAsList("[JUNCTIONS]")  # (list of Junction)
        self.reservoirs = SectionAsList("[RESERVOIRS]")  # (list of Reservoir)
        self.tanks = SectionAsList("[TANKS]")  # (list of Tank)
        self.pipes = SectionAsList("[PIPES]")  # (list of Pipe)
        self.pumps = SectionAsList("[PUMPS]")  # (list of Pump)
        self.valves = SectionAsList("[VALVES]")  # (list of Valve)
        # self.emitters = [(Junction, "emitter_coefficient")]
        self.patterns = SectionAsList("[PATTERNS]")  # (list of Pattern)
        self.curves = SectionAsList("[CURVES]")  # (list of Curve)
        self.energy = EnergyOptions()
        self.status = SectionAsList("[STATUS]")  # (list of Status)
        self.controls = Control()
        self.rules = Rule()
        self.demands = SectionAsList("[DEMANDS]")  # (list of Demand)
        self.reactions = Reactions()
        self.sources = SectionAsList("[SOURCES]")  # (list of Source)
        # self.options = MapOptions,
        self.options = Options()
        self.times = TimesOptions()
        self.report = ReportOptions()
        self.labels = SectionAsList("[LABELS]")  # (list of Label)
        self.backdrop = BackdropOptions()
        self.calibrations = SectionAsList("[CALIBRATIONS]") # (list of Calibration)

        self.sections = [
            self.title,
            self.options,
            self.report,
            self.junctions,
            self.tanks,
            self.reservoirs,
            self.pipes,
            self.pumps,
            self.valves,
            self.controls,
            self.patterns,
            self.curves,
            self.backdrop,
            self.map,
            self.labels]  # Start with a sensible order of sections.
        self.add_sections_from_attributes()  # Add any sections not added in the line above, should not be any left.

    def nodes_groups(self):
        return [self.junctions, self.reservoirs, self.tanks]

    def links_groups(self):
        return [self.pipes, self.pumps, self.valves]
