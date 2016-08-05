from core.inp_reader_base import InputFileReader, SectionReaderAsListOf, SectionReaderAsListGroupByID
# from core.swmm.hydraulics.control import ControlRule
from core.swmm.hydraulics.node import Junction, Outfall, Divider, StorageUnit
from core.swmm.hydraulics.node import DirectInflow, DryWeatherInflow, RDIInflow, Treatment
from core.swmm.hydraulics.link import Conduit, Pump, Orifice, Weir, Outlet, CrossSection, Transects
from core.swmm.title import Title
from core.swmm.options.general import General
# from core.swmm.options.time_steps import TimeSteps
from core.swmm.options.report import Report
from core.swmm.options.files import Files
from core.swmm.options.backdrop import BackdropOptions
from core.swmm.options.map import MapOptions
from core.swmm.climatology import Evaporation
from core.swmm.climatology import Temperature
from core.swmm.climatology import Adjustments
from core.swmm.curves import Curve
from core.swmm.hydrology.aquifer import Aquifer
from core.swmm.hydrology.lidcontrol import LIDControl
from core.swmm.hydrology.raingage import RainGage
from core.swmm.hydrology.snowpack import SnowPack
from core.swmm.hydrology.unithydrograph import UnitHydrograph
from core.swmm.hydrology.subcatchment import Subcatchment, LIDUsage, Groundwater, InitialLoadings, Coverages
from core.swmm.hydrology.subcatchment import HortonInfiltration, GreenAmptInfiltration, CurveNumberInfiltration
from core.swmm.patterns import Pattern
from core.swmm.timeseries import TimeSeries
from core.swmm.labels import Label
from core.swmm.quality import Landuse, Buildup, Washoff, Pollutant

from core.swmm.inp_reader_sections import *

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


class ProjectReader(InputFileReader):
    """Read a SWMM input file into in-memory data structures"""

    def __init__(self):
        """Define the fields of a SWMM Project by creating an empty placeholder for each section"""

        self.read_title = TitleReader()               # TITLE         project title
        self.read_options = GeneralReader()           # OPTIONS       analysis options
        self.read_report = ReportReader()             # REPORT        output reporting instructions
        # self.read_files = FilesReader()             # FILES         interface file options
        self.read_backdrop = BackdropOptionsReader()  # BACKDROP      bounding rectangle and file name of backdrop image
        self.read_map = MapOptionsReader()            # MAP           map's bounding rectangle and units
        self.read_raingages = SectionReaderAsListOf("[RAINGAGES]", RainGage, RainGageReader,
             ";;Name          \tFormat   \tInterval\tSCF     \tSource    \n"
             ";;--------------\t---------\t------  \t------  \t----------")

        self.read_hydrographs = SectionReaderAsListGroupByID("[HYDROGRAPHS]", UnitHydrograph, UnitHydrographReader,
            ";;Hydrograph    \tRain Gage/Month \tResponse\tR       \tT       \tK       \tDmax    \tDrecov  \tDinit   \n"
            ";;--------------\t----------------\t--------\t--------\t--------\t--------\t--------\t--------\t--------")
        # unit hydrograph data used to construct RDII inflows

        self.read_evaporation = EvaporationReader()        # EVAPORATION   evaporation data
        self.read_temperature = TemperatureReader()        # TEMPERATURE   air temperature and snow melt data
        self.read_adjustments = AdjustmentsReader()        # ADJUSTMENTS   monthly climate adjustments
        self.read_subcatchments = SectionReaderAsListOf("[SUBCATCHMENTS]", Subcatchment, SubcatchmentReader,
            ";;Name          \tRain Gage       \tOutlet          \tArea    \t%Imperv \tWidth   \t%Slope  \tCurbLen \tSnowPack        \n"
            ";;--------------\t----------------\t----------------\t--------\t--------\t--------\t--------\t--------\t----------------")
        # basic subcatchment information

        # self.read_subareas = [Section]               # SUBAREAS      subcatchment impervious/pervious sub-area data

        self.read_infiltration = SectionReaderAsListOf("[INFILTRATION]", basestring, None, None)
        # This is set to SectionReaderAsListOf HortonInfiltration or GreenAmptInfiltration or CurveNumberInfiltration
        # below in add_section based on subcatchment infiltration parameters

        self.read_lid_controls = SectionReaderAsListGroupByID("[LID_CONTROLS]", LIDControl, LIDControlReader,
                                                   ";;Name          \tType/Layer\tParameters\n"
                                                   ";;--------------\t----------\t----------")
        # low impact development control information

        self.read_lid_usage = SectionReaderAsListOf("[LID_USAGE]", LIDUsage, LIDUsageReader,
            ";;Subcatchment  \tLID Process     \tNumber \tArea      \tWidth     \tInitSat   \tFromImp   \tToPerv    \tRptFile                 \tDrainTo\n"
            ";;--------------\t----------------\t-------\t----------\t----------\t----------\t----------\t----------\t------------------------\t----------------")
        # assignment of LID controls to subcatchments

        self.read_aquifers = SectionReaderAsListOf("[AQUIFERS]", Aquifer, AquiferReader,
            ";;Aquifer       \tPhi   \tWP    \tFC    \tHydCon\tKslope\tTslope\tUEF   \tLED   \tLGLR  \tBEL   \tWTEL  \tUZM   \tUEF Pat\n"
            ";;--------------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t-------")
        # groundwater aquifer parameters

        self.read_groundwater = SectionReaderAsListOf("[GROUNDWATER]", Groundwater, GroundwaterReader,
            ";;Subcatchment  \tAquifer         \tNode            \tEsurf \tA1    \tB1    \tA2    \tB2    \tA3    \tDsw   \tEgwt  \tEbot  \tWgr   \tUmc   \n"
            ";;--------------\t----------------\t----------------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t------")
        # subcatchment groundwater parameters

        self.read_snowpacks = SectionReaderAsListGroupByID("[SNOWPACKS]", SnowPack, SnowPackReader,
                                                ";;Name          \tSurface   \tParameters\n"
                                                ";;--------------\t----------\t----------")
        # subcatchment snow pack parameters

        self.read_junctions = SectionReaderAsListOf("[JUNCTIONS]", Junction, JunctionReader,
                                         ";;Name          \tElevation \tMaxDepth  \tInitDepth \tSurDepth  \tAponded\n"
                                         ";;--------------\t----------\t----------\t----------\t----------\t----------")
        # junction node information

        self.read_outfalls = SectionReaderAsListOf("[OUTFALLS]", Outfall, SectionReader,
                                         ";;Name          \tElevation \tType      \tStage Data      \tGated   \tRoute To\n"
                                         ";;--------------\t----------\t----------\t----------------\t--------\t----------------")
        #  outfall node information

        self.read_dividers = SectionReaderAsListOf("[DIVIDERS]", Divider, SectionReader,
                                         ";;Name          \tElevation \tDiverted Link   \tType      \tParameters\n"
                                         ";;--------------\t----------\t----------------\t----------\t----------")
        #  flow divider node information

        self.read_storage = SectionReaderAsListOf("[STORAGE]", StorageUnit, SectionReader,
                                         ";;Name          \tElev.   \tMaxDepth  \tInitDepth  \tShape     \tCurve Name/Params           \tN/A     \tFevap   \tPsi     \tKsat    \tIMD\n"
                                         ";;--------------\t--------\t----------\t-----------\t----------\t----------------------------\t--------\t--------\t--------\t--------\t--------")
        #  storage node information

        self.read_conduits = SectionReaderAsListOf("[CONDUITS]", Conduit, ConduitReader,
            ";;Name          \tFrom Node       \tTo Node         \tLength    \tRoughness \tInOffset  \tOutOffset \tInitFlow  \tMaxFlow\n"
            ";;--------------\t----------------\t----------------\t----------\t----------\t----------\t----------\t----------\t----------")
        # conduit link information

        self.read_pumps = SectionReaderAsListOf("[PUMPS]", Pump, PumpReader,
            ";;Name          \tFrom Node       \tTo Node         \tPump Curve      \tStatus  \tStartup \tShutoffn"
            ";;--------------\t----------------\t----------------\t----------------\t--------\t--------\t--------")
        # pump link information

        self.read_orifices = SectionReaderAsListOf("[ORIFICES]", Orifice, SectionReader,
            ";;Name          \tFrom Node       \tTo Node         \tType        \tOffset    \tQcoeff    \tGated   \tCloseTime\n"
            ";;--------------\t----------------\t----------------\t------------\t----------\t----------\t--------\t----------")
        # orifice link information

        self.read_weirs = SectionReaderAsListOf("[WEIRS]", Weir, SectionReader,
            ";;Name          \tFrom Node       \tTo Node         \tType        \tCrestHt   \tQcoeff    \tGated   \tEndCon  \tEndCoeff  \tSurcharge \tRoadWidth \tRoadSurf\n"
            ";;--------------\t----------------\t----------------\t------------\t----------\t----------\t--------\t--------\t----------\t----------\t----------\t----------")
        # weir link information

        self.read_outlets = SectionReaderAsListOf("[OUTLETS]", Outlet, SectionReader,
            ";;Name          \tFrom Node       \tTo Node         \tOffset    \tType           \tQTable/Qcoeff   \tQexpon    \tGated\n"
            ";;--------------\t----------------\t----------------\t----------\t---------------\t----------------\t----------\t--------")
        # outlet link information

        self.read_xsections = SectionReaderAsListOf("[XSECTIONS]", CrossSection, CrossSectionReader,
            ";;Link          \tShape       \tGeom1           \tGeom2     \tGeom3     \tGeom4     \tBarrels   \tCulvert   \n"
            ";;--------------\t------------\t----------------\t----------\t----------\t----------\t----------\t----------")
        # conduit, orifice, and weir cross-section geometry

        self.read_transects = TransectsReader() # TRANSECTS # transect geometry for conduits with irregular cross-sections
        # self.read_losses = [Section] # LOSSES # conduit entrance/exit losses and flap valves
        self.read_controls = SectionReaderAsListOf("[CONTROLS]", basestring, None, None)  # rules that control pump and regulator operation
        self.read_landuses = SectionReaderAsListOf("[LANDUSES]", Landuse, LanduseReader,
                                        ";;              \tSweeping  \tFraction  \tLast\n"
                                        ";;Name          \tInterval  \tAvailable \tSwept\n"
                                        ";;--------------\t----------\t----------\t----------")
        # land use categories

        self.read_buildup = SectionReaderAsListOf("[BUILDUP]", Buildup, BuildupReader,
            ";;Land Use      \tPollutant       \tFunction  \tCoeff1    \tCoeff2    \tCoeff3    \tPer Unit\n"
            ";;--------------\t----------------\t----------\t----------\t----------\t----------\t----------")
        # buildup functions for pollutants and land uses

        self.read_washoff = SectionReaderAsListOf("[WASHOFF]", Washoff, WashoffReader,
            ";;Land Use      \tPollutant       \tFunction  \tCoeff1    \tCoeff2    \tSweepRmvl \tBmpRmvl\n"
            ";;--------------\t----------------\t----------\t----------\t----------\t----------\t----------")
        # washoff functions for pollutants and land uses

        self.read_pollutants = SectionReaderAsListOf("[POLLUTANTS]", Pollutant, PollutantReader,
            ";;Name          \tUnits \tCrain     \tCgw       \tCrdii     \tKdecay    \tSnowOnly  \tCo-Pollutant    \tCo-Frac   \tCdwf      \tCinit\n"
            ";;--------------\t------\t----------\t----------\t----------\t----------\t----------\t----------------\t----------\t----------\t----------")
        # pollutant information

        self.read_coverages = CoveragesReader() # COVERAGES # assignment of land uses to subcatchments
        self.read_treatment = SectionReaderAsListOf("[TREATMENT]", Treatment, TreatmentReader,
                                         ";;Node          \tPollutant       \tFunction\n"
                                         ";;--------------\t----------------\t--------")

        # pollutant removal functions at conveyance system nodes

        self.read_inflows = SectionReaderAsListOf("[INFLOWS]", DirectInflow, DirectInflowReader,
            ";;Node          \tConstituent     \tTime Series     \tType    \tMfactor \tSfactor \tBaseline\tPattern\n"
            ";;--------------\t----------------\t----------------\t--------\t--------\t--------\t--------\t--------")
        # INFLOWS # external hydrograph/pollutograph inflow at nodes

        self.read_dwf = SectionReaderAsListOf("[DWF]", DryWeatherInflow, DryWeatherInflowReader,
                                   ";;Node          \tConstituent     \tBaseline  \tPatterns  \n"
                                   ";;--------------\t----------------\t----------\t----------")
        # baseline dry weather sanitary inflow at nodes

        self.read_patterns = SectionReaderAsListGroupByID("[PATTERNS]", Pattern, PatternReader,
                                               ";;Name          \tType      \tMultipliers\n"
                                               ";;--------------\t----------\t-----------")
        # PATTERNS      periodic variation in dry weather inflow

        self.read_rdii = SectionReaderAsListOf("[RDII]", RDIInflow, RDIInflowReader,
                                    ";;Node          \tUnit Hydrograph \tSewer Area\n"
                                    ";;--------------\t----------------\t----------")
        # rainfall-dependent I/I information at nodes

        self.read_loadings = InitialLoadingsReader()
        # initial pollutant loads on subcatchments

        self.read_curves = SectionReaderAsListGroupByID("[CURVES]", Curve, CurveReader,
                                             ";;Name          \tType      \tX-Value   \tY-Value   \n"
                                             ";;--------------\t----------\t----------\t----------")
        # CURVES        x-y tabular data referenced in other sections

        self.read_timeseries = SectionReaderAsListGroupByID("[TIMESERIES]", TimeSeries, TimeSeriesReader,
                                                 ";;Name          \tDate      \tTime      \tValue\n"
                                                 ";;--------------\t----------\t----------\t----------")
        # time series data referenced in other sections

        # self.read_labels = SectionReaderAsListGroupByID("[LABELS]", Label, LabelReader,
        #                                          ";;X-Coord         \tY-Coord           \tLabel\n")
        # X,Y coordinates and text of labels

        # self.read_polygons = [Section] # POLYGONS # X,Y coordinates for each vertex of subcatchment polygons
        # self.read_coordinates = [Section] # COORDINATES # X,Y coordinates for nodes
        # self.read_vertices = [Section] # VERTICES # X,Y coordinates for each interior vertex of polyline links
        # self.read_symbols = [Section] # SYMBOLS # X,Y coordinates for rain gages
        #  X,Y coordinates of the bounding rectangle and file name of the backdrop image.
        # [TAGS]

    def read_section(self, project, section_name, section_text):
        if section_name == project.infiltration.SECTION_NAME:
            infiltration = project.options.infiltration.upper()
            if infiltration == "HORTON":
                self.read_infiltration = SectionReaderAsListOf(
                    section_name, HortonInfiltration, HortonInfiltrationReader,
                    ";;Subcatchment  \tMaxRate   \tMinRate   \tDecay     \tDryTime   \tMaxInfiltration\n"
                    ";;--------------\t----------\t----------\t----------\t----------\t----------")
            elif infiltration.startswith("GREEN"):
                self.read_infiltration = SectionReaderAsListOf(
                    section_name, GreenAmptInfiltration, GreenAmptInfiltrationReader,
                    ";;Subcatchment  \tSuction   \tKsat      \tIMD       \n"
                    ";;--------------\t----------\t----------\t----------")
            elif infiltration.startswith("CURVE"):
                self.read_infiltration = SectionReaderAsListOf(
                    section_name, CurveNumberInfiltration, CurveNumberInfiltrationReader,
                    ";;Subcatchment  \tCurveNum  \t          \tDryTime   \n"
                    ";;--------------\t----------\t----------\t----------")
        InputFileReader.read_section(self, project, section_name, section_text)
