from core.inputfile import InputFile, SectionAsListOf
# from core.swmm.hydraulics.control import ControlRule
from core.swmm.hydraulics.node import Node, Junction, Outfall, Divider, StorageUnit
from core.swmm.hydraulics.link import Conduit, Pump, Orifice, Weir, Outlet, CrossSection, Transect
from core.swmm.title import Title
from core.swmm.options.general import General
# from core.swmm.options.time_steps import TimeSteps
from core.swmm.options.report import Report
from core.swmm.options.files import Files
from core.swmm.options.backdrop import BackdropOptions
from core.swmm.options.map import MapOptions
from core.swmm.climatology.climatology import Evaporation
from core.swmm.climatology.climatology import Temperature
from core.swmm.curves import Curves
from core.swmm.hydrology.aquifer import Aquifer
from core.swmm.hydrology.lidcontrol import LIDControls
from core.swmm.hydrology.raingage import RainGage
from core.swmm.hydrology.unithydrograph import UnitHydrograph
from core.swmm.hydrology.subcatchment import Subcatchment
from core.swmm.patterns import Patterns
from core.swmm.timeseries import TimeSeries
from core.swmm.quality import Landuse, Buildup, Washoff, Pollutant


class Project(InputFile):
    """Manage a complete SWMM input sequence"""

    # section_types = {
    #     "[TITLE]": None,  # project title
    #     "[OPTIONS]": core.swmm.options.general.General(),  # analysis options
    #     "[REPORT]": None,  # output reporting instructions
    #     "[FILES]": core.swmm.files.Files,  # interface file options
    #     "[RAINGAGES]": [core.swmm.hydrology.raingage.RainGage],  # rain gage information
    #     "[HYDROGRAPHS]": None,  # unit hydrograph data used to construct RDII inflows
    #     "[EVAPORATION]": None,  # evaporation data
    #     "[TEMPERATURE]": None,  # air temperature and snow melt data
    #     "[SUBCATCHMENTS]": [core.swmm.hydrology.subcatchment.Subcatchment],  # basic subcatchment information
    #     "[SUBAREAS]": None,  # subcatchment impervious/pervious sub-area data
    #     "[INFILTRATION]": None,  # subcatchment infiltration parameters
    #     "[LID_CONTROLS]": None,  # low impact development control information
    #     "[LID_USAGE]": None,  # assignment of LID controls to subcatchments
    #     "[AQUIFERS]": None,  # groundwater aquifer parameters
    #     "[GROUNDWATER]": None,  # subcatchment groundwater parameters
    #     "[SNOWPACKS]": None,  # subcatchment snow pack parameters
    #     "[JUNCTIONS]": [core.swmm.hydraulics.node.Junction],  # junction node information
    #     "[OUTFALLS]": None,  # outfall node information
    #     "[DIVIDERS]": None,  # flow divider node information
    #     "[STORAGE]": None,  # storage node information
    #     "[CONDUITS]": [core.swmm.hydraulics.link.Conduit],  # conduit link information
    #     "[PUMPS]": None,  # pump link information
    #     "[ORIFICES]": None,  # orifice link information
    #     "[WEIRS]": None,  # weir link information
    #     "[OUTLETS]": None,  # outlet link information
    #     "[XSECTIONS]": [core.swmm.hydraulics.link.CrossSection],  # conduit, orifice, and weir cross-section geometry
    #     "[TRANSECTS]": None,  # transect geometry for conduits with irregular cross-sections
    #     "[LOSSES]": None,  # conduit entrance/exit losses and flap valves
    #     "[CONTROLS]": None,  # rules that control pump and regulator operation
    #     "[POLLUTANTS]": None,  # pollutant information
    #     "[LANDUSES]": None,  # land use categories
    #     "[COVERAGES]": None,  # assignment of land uses to subcatchments
    #     "[BUILDUP]": None,  # buildup functions for pollutants and land uses
    #     "[WASHOFF]": None,  # washoff functions for pollutants and land uses
    #     "[TREATMENT]": None,  # pollutant removal functions at conveyance system nodes
    #     "[INFLOWS]": None,  # external hydrograph/pollutograph inflow at nodes
    #     "[DWF]": None,  # baseline dry weather sanitary inflow at nodes
    #     "[PATTERNS]": None,  # periodic variation in dry weather inflow
    #     "[RDII]": None,  # rainfall-dependent I/I information at nodes
    #     "[LOADINGS]": None,  # initial pollutant loads on subcatchments
    #     "[CURVES]": None,  # x-y tabular data referenced in other sections
    #     "[TIMESERIES]": None,  # time series data referenced in other sections
    #
    #     "[MAP]": None,       # X,Y coordinates of the map's bounding rectangle
    #     "[POLYGONS]": None,  # X,Y coordinates for each vertex of subcatchment polygons
    #     "[COORDINATES]": [core.coordinates.Coordinates],  # X,Y coordinates for nodes
    #     "[VERTICES]": None,  # X,Y coordinates for each interior vertex of polyline links
    #     "[LABELS]": None,    # X,Y coordinates and text of labels
    #     "[SYMBOLS]": None,   # X,Y coordinates for rain gages
    #     "[BACKDROP]": None   # X,Y coordinates of the bounding rectangle and file name of the backdrop image.
    #     # [TAGS]
    #     }

    def __init__(self):
        """Define the fields of a SWMM Project by creating an empty placeholder for each section"""

        self.title = Title()                    # TITLE         project title
        self.options = General()                # OPTIONS       analysis options
        self.report = Report()                  # REPORT        output reporting instructions
        self.files = Files()                    # FILES         interface file options
        self.backdrop = BackdropOptions()       # BACKDROP      bounding rectangle and file name of backdrop image
        self.map = MapOptions()                 # MAP           map's bounding rectangle and units
        # self.raingages = [RainGage]             # RAINGAGES     rain gage information
        # self.hydrographs = [UnitHydrograph]     # HYDROGRAPHS   unit hydrograph data used to construct RDII inflows
        # self.evaporation = Evaporation()        # EVAPORATION   evaporation data
        # self.temperature = Temperature()        # TEMPERATURE   air temperature and snow melt data
        # self.subcatchments = [Subcatchment]     # SUBCATCHMENTS basic subcatchment information
        # self.subareas = [Section]               # SUBAREAS      subcatchment impervious/pervious sub-area data
        # self.infiltration = [Section]           # INFILTRATION  subcatchment infiltration parameters
        self.lid_controls = LIDControls()  # low impact development control information
        # self.lid_usage = [Section]              # LID_USAGE     assignment of LID controls to subcatchments
        self.aquifers = SectionAsListOf("[AQUIFERS]", Aquifer)  # groundwater aquifer parameters
        # self.groundwater = [Section]            # GROUNDWATER   subcatchment groundwater parameters
        # self.snowpacks = [Section]              # SNOWPACKS     subcatchment snow pack parameters
        # self.junctions = [Junction]             # JUNCTIONS     junction node information
        # self.outfalls = [Outfall] # OUTFALLS # outfall node information
        # self.dividers = [Divider] # DIVIDERS # flow divider node information
        # self.storage = [StorageUnit] # STORAGE # storage node information
        # self.conduits = [Conduit] # CONDUITS # conduit link information
        # self.pumps = [Pump] # PUMPS # pump link information
        # self.orifices = [Orifice] # ORIFICES # orifice link information
        # self.weirs = [Weir] # WEIRS # weir link information
        # self.outlets = [Outlet] # OUTLETS # outlet link information
        # self.xsections = [CrossSection] # XSECTIONS # conduit, orifice, and weir cross-section geometry
        # self.transects = [Transect] # TRANSECTS # transect geometry for conduits with irregular cross-sections
        # self.losses = [Section] # LOSSES # conduit entrance/exit losses and flap valves
        self.controls = SectionAsListOf("[CONTROLS]", basestring) # rules that control pump and regulator operation
        self.landuses = SectionAsListOf("[LANDUSES]", Landuse)    # land use categories
        self.buildup = SectionAsListOf("[BUILDUP]", Buildup)      # buildup functions for pollutants and land uses
        self.washoff = SectionAsListOf("[WASHOFF]", Washoff)      # washoff functions for pollutants and land uses
        self.pollutants = SectionAsListOf("[POLLUTANTS]", Pollutant)  # pollutant information
        # self.coverages = [Section] # COVERAGES # assignment of land uses to subcatchments
        # self.treatment = [Section] # TREATMENT # pollutant removal functions at conveyance system nodes
        # self.inflows = [Section] # INFLOWS # external hydrograph/pollutograph inflow at nodes
        # self.dwf = [Section]                    # DWF           baseline dry weather sanitary inflow at nodes
        self.patterns = Patterns()                # PATTERNS      periodic variation in dry weather inflow
        # self.rdii = [Section]                   # RDII          rainfall-dependent I/I information at nodes
        # self.loadings = [Section]               # LOADINGS      initial pollutant loads on subcatchments
        self.curves = Curves()                    # CURVES        x-y tabular data referenced in other sections
        # self.timeseries = [TimeSeries] # TIMESERIES # time series data referenced in other sections
        # self.polygons = [Section] # POLYGONS # X,Y coordinates for each vertex of subcatchment polygons
        # self.coordinates = [Section] # COORDINATES # X,Y coordinates for nodes
        # self.vertices = [Section] # VERTICES # X,Y coordinates for each interior vertex of polyline links
        # self.labels = [Section] # LABELS # X,Y coordinates and text of labels
        # self.symbols = [Section] # SYMBOLS # X,Y coordinates for rain gages
        #  X,Y coordinates of the bounding rectangle and file name of the backdrop image.
        # [TAGS]
        InputFile.__init__(self)  # Do this after setting attributes so they will all get added to sections[]

