from core.coordinate import Coordinate
from core.project_base import ProjectBase, SectionAsList
from core.swmm.climatology import Adjustments
from core.swmm.climatology import Evaporation
from core.swmm.climatology import Temperature
from core.swmm.curves import Curve
from core.swmm.hydraulics.control import Controls
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
from core.indexed_list import IndexedList

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
        self.raingages = SectionAsList("[RAINGAGES]")  # (list of RainGage)  # RAINGAGES  rain gage information

        self.hydrographs = SectionAsList("[HYDROGRAPHS]")  # (list of UnitHydrograph)
        # unit hydrograph data used to construct RDII inflows

        self.evaporation = Evaporation()        # EVAPORATION   evaporation data
        self.temperature = Temperature()        # TEMPERATURE   air temperature and snow melt data
        self.adjustments = Adjustments()        # ADJUSTMENTS   monthly climate adjustments
        self.subcatchments = SectionAsList("[SUBCATCHMENTS]")  # (list of Subcatchment)
        # basic subcatchment information

        # self.subareas = [Section]               # SUBAREAS      subcatchment impervious/pervious sub-area data

        self.infiltration = SectionAsList("[INFILTRATION]")  # (list of basestring)
        # subcatchment infiltration parameters

        self.lid_controls = SectionAsList("[LID_CONTROLS]")  # (list of LIDControl)
        # low impact development control information

        self.lid_usage = SectionAsList("[LID_USAGE]")  # (list of LIDUsage)
        # assignment of LID controls to subcatchments

        self.aquifers = SectionAsList("[AQUIFERS]")  # (list of Aquifer)
        # groundwater aquifer parameters

        self.groundwater = SectionAsList("[GROUNDWATER]")  # (list of Groundwater)
        # subcatchment groundwater parameters

        self.snowpacks = SectionAsList("[SNOWPACKS]")  # (list of SnowPack)
        # subcatchment snow pack parameters

        self.junctions = SectionAsList("[JUNCTIONS]")  # (list of Junction)
        # junction node information

        self.outfalls = SectionAsList("[OUTFALLS]")  # (list of Outfall)
        #  outfall node information

        self.dividers = SectionAsList("[DIVIDERS]")  # (list of Divider)
        #  flow divider node information

        self.storage = SectionAsList("[STORAGE]")  # (list of StorageUnit)
        #  storage node information

        self.conduits = SectionAsList("[CONDUITS]")  # (list of Conduit)
        # conduit link information

        self.pumps = SectionAsList("[PUMPS]")  # (list of Pump)
        # pump link information

        self.orifices = SectionAsList("[ORIFICES]")  # (list of Orifice)
        # orifice link information

        self.weirs = SectionAsList("[WEIRS]")  # (list of Weir)
        # weir link information

        self.outlets = SectionAsList("[OUTLETS]")  # (list of Outlet)
        # outlet link information

        self.xsections = SectionAsList("[XSECTIONS]")  # (list of CrossSection)
        # conduit, orifice, and weir cross-section geometry

        self.transects = Transects()  # transect geometry for conduits with irregular cross-sections

        self.controls = Controls()
        # rules that control pump and regulator operation

        self.landuses = SectionAsList("[LANDUSES]")  # (list of Landuse)     # land use categories

        self.buildup = SectionAsList("[BUILDUP]")  # (list of Buildup)
        # buildup functions for pollutants and land uses

        self.washoff = SectionAsList("[WASHOFF]")  # (list of Washoff)
        # washoff functions for pollutants and land uses

        self.pollutants = SectionAsList("[POLLUTANTS]")  # (list of Pollutant)
        # pollutant information

        self.coverages = Coverages() # COVERAGES   assignment of land uses to subcatchments
        self.treatment = SectionAsList("[TREATMENT]")  # (list of Treatment)
        # pollutant removal functions at conveyance system nodes

        self.inflows = SectionAsList("[INFLOWS]")  # (list of DirectInflow)
        # INFLOWS # external hydrograph/pollutograph inflow at nodes

        self.dwf = SectionAsList("[DWF]")  # (list of DryWeatherInflow)
        # baseline dry weather sanitary inflow at nodes

        self.patterns = SectionAsList("[PATTERNS]")  # (list of Pattern)
        # periodic variation in dry weather inflow

        self.rdii = SectionAsList("[RDII]")  # (list of RDIInflow)
        # rainfall-dependent I/I information at nodes

        self.loadings = InitialLoadings()
        # initial pollutant loads on subcatchments

        self.curves = SectionAsList("[CURVES]")  # (list of Curve)
        # CURVES        x-y tabular data referenced in other sections

        self.timeseries = SectionAsList("[TIMESERIES]")  # (list of TimeSeries)
        # time series data referenced in other sections

        self.labels = SectionAsList("[LABELS]")  # (list of Label)
        # X, Y coordinates and text of labels

        self.polygons = SectionAsList("[POLYGONS]")  # (list of Coordinate)
        # X, Y coordinates for each vertex of subcatchment polygons

        self.vertices = SectionAsList("[VERTICES]")  # (list of Coordinate)
        # X,Y coordinates for each interior vertex of polyline links

        ProjectBase.__init__(self)  # Do this after setting attributes so they will all get added to sections[]

    def nodes_groups(self):
        return [self.junctions, self.outfalls, self.dividers, self.storage]

    def all_coordinates(self):
        all = IndexedList([], ['name'])
        for section in self.nodes_groups():
            all.extend(section.value)
        return all

    def links_groups(self):
        return [self.conduits, self.pumps, self.orifices, self.weirs, self.outlets]
