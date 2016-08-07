from core.coordinate import Coordinate
from core.project_base import ProjectBase, SectionAsListOf
from core.swmm.climatology import Adjustments
from core.swmm.climatology import Evaporation
from core.swmm.climatology import Temperature
from core.swmm.curves import Curve
from core.swmm.hydraulics.link import Conduit, Pump, Orifice, Weir, Outlet, CrossSection, Transects
from core.swmm.hydraulics.node import DirectInflow, DryWeatherInflow, RDIInflow, Treatment
from core.swmm.hydraulics.node import Junction, Outfall, Divider, StorageUnit
from core.swmm.hydrology.aquifer import Aquifer
from core.swmm.hydrology.lidcontrol import LIDControl
from core.swmm.hydrology.raingage import RainGage
from core.swmm.hydrology.snowpack import SnowPack
from core.swmm.hydrology.subcatchment import HortonInfiltration, GreenAmptInfiltration, CurveNumberInfiltration
from core.swmm.hydrology.subcatchment import Subcatchment, LIDUsage, Groundwater, InitialLoadings, Coverages
from core.swmm.hydrology.unithydrograph import UnitHydrograph
from core.swmm.labels import Label
from core.swmm.options.backdrop import BackdropOptions
from core.swmm.options.files import Files
from core.swmm.options.general import General
from core.swmm.options.map import MapOptions
from core.swmm.options.report import Report
from core.swmm.patterns import Pattern
from core.swmm.quality import Landuse, Buildup, Washoff, Pollutant
from core.swmm.timeseries import TimeSeries
from core.swmm.title import Title

try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str, bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring


class SwmmProject(ProjectBase):
    """Manage a complete SWMM input sequence"""

    def __init__(self):
        """Define the fields of a SWMM Project by creating an empty placeholder for each section"""

        self.title = Title()                    # TITLE         project title
        self.options = General()                # OPTIONS       analysis options
        self.report = Report()                  # REPORT        output reporting instructions
        self.files = Files()                    # FILES         interface file options
        self.backdrop = BackdropOptions()       # BACKDROP      bounding rectangle and file name of backdrop image
        self.map = MapOptions()                 # MAP           map's bounding rectangle and units
        self.raingages = SectionAsListOf("[RAINGAGES]", RainGage)  # RAINGAGES  rain gage information

        self.hydrographs = SectionAsListOf("[HYDROGRAPHS]", UnitHydrograph)
        # unit hydrograph data used to construct RDII inflows

        self.evaporation = Evaporation()        # EVAPORATION   evaporation data
        self.temperature = Temperature()        # TEMPERATURE   air temperature and snow melt data
        self.adjustments = Adjustments()        # ADJUSTMENTS   monthly climate adjustments
        self.subcatchments = SectionAsListOf("[SUBCATCHMENTS]", Subcatchment)
        # basic subcatchment information

        # self.subareas = [Section]               # SUBAREAS      subcatchment impervious/pervious sub-area data

        self.infiltration = SectionAsListOf("[INFILTRATION]", basestring)
        # This is set to SectionAsListOf HortonInfiltration or GreenAmptInfiltration or CurveNumberInfiltration on read
        # subcatchment infiltration parameters

        self.lid_controls = SectionAsListOf("[LID_CONTROLS]", LIDControl)
        # low impact development control information

        self.lid_usage = SectionAsListOf("[LID_USAGE]", LIDUsage)
        # assignment of LID controls to subcatchments

        self.aquifers = SectionAsListOf("[AQUIFERS]", Aquifer)
        # groundwater aquifer parameters

        self.groundwater = SectionAsListOf("[GROUNDWATER]", Groundwater)
        # subcatchment groundwater parameters

        self.snowpacks = SectionAsListOf("[SNOWPACKS]", SnowPack)
        # subcatchment snow pack parameters

        self.junctions = SectionAsListOf("[JUNCTIONS]", Junction)
        # junction node information

        self.outfalls = SectionAsListOf("[OUTFALLS]", Outfall)
        #  outfall node information

        self.dividers = SectionAsListOf("[DIVIDERS]", Divider)
        #  flow divider node information

        self.storage = SectionAsListOf("[STORAGE]", StorageUnit)
        #  storage node information

        self.conduits = SectionAsListOf("[CONDUITS]", Conduit)
        # conduit link information

        self.pumps = SectionAsListOf("[PUMPS]", Pump)
        # pump link information

        self.orifices = SectionAsListOf("[ORIFICES]", Orifice)
        # orifice link information

        self.weirs = SectionAsListOf("[WEIRS]", Weir)
        # weir link information

        self.outlets = SectionAsListOf("[OUTLETS]", Outlet)
        # outlet link information

        self.xsections = SectionAsListOf("[XSECTIONS]", CrossSection)
        # conduit, orifice, and weir cross-section geometry

        self.transects = Transects() # TRANSECTS   transect geometry for conduits with irregular cross-sections
        # self.losses = [Section] # LOSSES   conduit entrance/exit losses and flap valves
        self.controls = SectionAsListOf("[CONTROLS]", basestring)  # rules that control pump and regulator operation
        self.landuses = SectionAsListOf("[LANDUSES]", Landuse)     # land use categories

        self.buildup = SectionAsListOf("[BUILDUP]", Buildup)
        # buildup functions for pollutants and land uses

        self.washoff = SectionAsListOf("[WASHOFF]", Washoff)
        # washoff functions for pollutants and land uses

        self.pollutants = SectionAsListOf("[POLLUTANTS]", Pollutant)
        # pollutant information

        self.coverages = Coverages() # COVERAGES   assignment of land uses to subcatchments
        self.treatment = SectionAsListOf("[TREATMENT]", Treatment)
        # pollutant removal functions at conveyance system nodes

        self.inflows = SectionAsListOf("[INFLOWS]", DirectInflow)
        # INFLOWS # external hydrograph/pollutograph inflow at nodes

        self.dwf = SectionAsListOf("[DWF]", DryWeatherInflow)
        # baseline dry weather sanitary inflow at nodes

        self.patterns = SectionAsListOf("[PATTERNS]", Pattern)
        # PATTERNS      periodic variation in dry weather inflow

        self.rdii = SectionAsListOf("[RDII]", RDIInflow)
        # rainfall-dependent I/I information at nodes

        self.loadings = InitialLoadings()
        # initial pollutant loads on subcatchments

        self.curves = SectionAsListOf("[CURVES]", Curve)
        # CURVES        x-y tabular data referenced in other sections

        self.timeseries = SectionAsListOf("[TIMESERIES]", TimeSeries)
        # time series data referenced in other sections

        self.labels = SectionAsListOf("[LABELS]", Label)
        # X,Y coordinates and text of labels

        self.polygons = SectionAsListOf("[POLYGONS]", Coordinate)
        # X,Y coordinates for each vertex of subcatchment polygons

        self.coordinates = SectionAsListOf("[COORDINATES]", Coordinate)  # X,Y coordinates for nodes

        # self.vertices = [Section] # VERTICES # X,Y coordinates for each interior vertex of polyline links
        # self.symbols = [Section] # SYMBOLS # X,Y coordinates for rain gages
        #  X,Y coordinates of the bounding rectangle and file name of the backdrop image.
        # [TAGS]
        ProjectBase.__init__(self)  # Do this after setting attributes so they will all get added to sections[]

    def add_section(self, section_name, section_text):
        if section_name == self.infiltration.SECTION_NAME:
            if self.options.infiltration.upper() == "HORTON":
                self.infiltration = SectionAsListOf(self.infiltration.SECTION_NAME, HortonInfiltration)
            elif self.options.infiltration.upper().startswith("GREEN"):
                self.infiltration = SectionAsListOf(self.infiltration.SECTION_NAME, GreenAmptInfiltration)
            elif self.options.infiltration.upper().startswith("CURVE"):
                self.infiltration = SectionAsListOf(self.infiltration.SECTION_NAME, CurveNumberInfiltration)
        ProjectBase.add_section(self, section_name, section_text)
