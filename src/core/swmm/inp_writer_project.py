from core.inp_writer_base import InputFileWriterBase, SectionWriterAsListOf, SectionAsListOf
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

from core.swmm.inp_writer_sections import *

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
    """Write a SWMM input file from in-memory data structures"""

    def __init__(self):
        """Define the fields of a SWMM Project by creating an empty placeholder for each section"""

        self.write_title = TitleWriter()               # TITLE         project title
        self.write_options = GeneralWriter()           # OPTIONS       analysis options
        self.write_report = ReportWriter()             # REPORT        output reporting instructions
        # self.write_files = FilesWriter()             # FILES         interface file options
        self.write_backdrop = BackdropOptionsWriter()  # BACKDROP      bounding rectangle and file name of backdrop image
        self.write_map = MapOptionsWriter()            # MAP           map's bounding rectangle and units
        self.write_raingages = SectionWriterAsListOf("[RAINGAGES]", RainGage, RainGageWriter,
             ";;Name          \tFormat   \tInterval\tSCF     \tSource    \n"
             ";;--------------\t---------\t------  \t------  \t----------")

        self.write_hydrographs = SectionWriterAsListOf("[HYDROGRAPHS]", UnitHydrograph, UnitHydrographWriter,
            ";;Hydrograph    \tRain Gage/Month \tResponse\tR       \tT       \tK       \tDmax    \tDrecov  \tDinit   \n"
            ";;--------------\t----------------\t--------\t--------\t--------\t--------\t--------\t--------\t--------")
        # unit hydrograph data used to construct RDII inflows

        self.write_evaporation = EvaporationWriter()        # EVAPORATION   evaporation data
        self.write_temperature = TemperatureWriter()        # TEMPERATURE   air temperature and snow melt data
        self.write_adjustments = AdjustmentsWriter()        # ADJUSTMENTS   monthly climate adjustments
        self.write_subcatchments = SectionWriterAsListOf("[SUBCATCHMENTS]", Subcatchment, SubcatchmentWriter,
            ";;Name          \tRain Gage       \tOutlet          \tArea    \t%Imperv \tWidth   \t%Slope  \tCurbLen \tSnowPack        \n"
            ";;--------------\t----------------\t----------------\t--------\t--------\t--------\t--------\t--------\t----------------")
        # basic subcatchment information

        self.write_subareas = SectionWriterAsListOf("[SUBAREAS]", Subcatchment, SubareaWriter,
            ";;Subcatchment  \tN-Imperv  \tN-Perv    \tS-Imperv  \tS-Perv    \tPctZero   \tRouteTo   \tPctRouted\n"
            ";;--------------\t----------\t------------\t--------\t----------\t----------\t----------\t---------")
        # subcatchment impervious/pervious sub-area data

        #self.write_infiltration = SectionWriterAsListOf("[INFILTRATION]", basestring, SectionWriter, None)
        # write_infiltration is set in as_text based on the kind of infiltration being used in the project.

        self.write_lid_controls = SectionWriterAsListOf("[LID_CONTROLS]", LIDControl, LIDControlWriter,
                                                   ";;Name          \tType/Layer\tParameters\n"
                                                   ";;--------------\t----------\t----------")
        # low impact development control information

        self.write_lid_usage = SectionWriterAsListOf("[LID_USAGE]", LIDUsage, LIDUsageWriter,
            ";;Subcatchment  \tLID Process     \tNumber \tArea      \tWidth     \tInitSat   \tFromImp   \tToPerv    \tRptFile                 \tDrainTo\n"
            ";;--------------\t----------------\t-------\t----------\t----------\t----------\t----------\t----------\t------------------------\t----------------")
        # assignment of LID controls to subcatchments

        self.write_aquifers = SectionWriterAsListOf("[AQUIFERS]", Aquifer, AquiferWriter,
            ";;Aquifer       \tPhi   \tWP    \tFC    \tHydCon\tKslope\tTslope\tUEF   \tLED   \tLGLR  \tBEL   \tWTEL  \tUZM   \tUEF Pat\n"
            ";;--------------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t-------")
        # groundwater aquifer parameters

        self.write_groundwater = SectionWriterAsListOf("[GROUNDWATER]", Groundwater, GroundwaterWriter,
            ";;Subcatchment  \tAquifer         \tNode            \tEsurf \tA1    \tB1    \tA2    \tB2    \tA3    \tDsw   \tEgwt  \tEbot  \tWgr   \tUmc   \n"
            ";;--------------\t----------------\t----------------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t------")
        # subcatchment groundwater parameters

        self.write_snowpacks = SectionWriterAsListOf("[SNOWPACKS]", SnowPack, SnowPackWriter,
                                                ";;Name          \tSurface   \tParameters\n"
                                                ";;--------------\t----------\t----------")
        # subcatchment snow pack parameters

        self.write_junctions = SectionWriterAsListOf("[JUNCTIONS]", Junction, JunctionWriter,
                                         ";;Name          \tElevation \tMaxDepth  \tInitDepth \tSurDepth  \tAponded\n"
                                         ";;--------------\t----------\t----------\t----------\t----------\t----------")
        # junction node information

        self.write_outfalls = SectionWriterAsListOf("[OUTFALLS]", Outfall, SectionWriter,
                                         ";;Name          \tElevation \tType      \tStage Data      \tGated   \tRoute To\n"
                                         ";;--------------\t----------\t----------\t----------------\t--------\t----------------")
        #  outfall node information

        self.write_dividers = SectionWriterAsListOf("[DIVIDERS]", Divider, SectionWriter,
                                         ";;Name          \tElevation \tDiverted Link   \tType      \tParameters\n"
                                         ";;--------------\t----------\t----------------\t----------\t----------")
        #  flow divider node information

        self.write_storage = SectionWriterAsListOf("[STORAGE]", StorageUnit, SectionWriter,
                                         ";;Name          \tElev.   \tMaxDepth  \tInitDepth  \tShape     \tCurve Name/Params           \tN/A     \tFevap   \tPsi     \tKsat    \tIMD\n"
                                         ";;--------------\t--------\t----------\t-----------\t----------\t----------------------------\t--------\t--------\t--------\t--------\t--------")
        #  storage node information

        self.write_conduits = SectionWriterAsListOf("[CONDUITS]", Conduit, ConduitWriter,
            ";;Name          \tFrom Node       \tTo Node         \tLength    \tRoughness \tInOffset  \tOutOffset \tInitFlow  \tMaxFlow\n"
            ";;--------------\t----------------\t----------------\t----------\t----------\t----------\t----------\t----------\t----------")
        # conduit link information

        self.write_pumps = SectionWriterAsListOf("[PUMPS]", Pump, PumpWriter,
            ";;Name          \tFrom Node       \tTo Node         \tPump Curve      \tStatus  \tStartup \tShutoffn"
            ";;--------------\t----------------\t----------------\t----------------\t--------\t--------\t--------")
        # pump link information

        self.write_orifices = SectionWriterAsListOf("[ORIFICES]", Orifice, SectionWriter,
            ";;Name          \tFrom Node       \tTo Node         \tType        \tOffset    \tQcoeff    \tGated   \tCloseTime\n"
            ";;--------------\t----------------\t----------------\t------------\t----------\t----------\t--------\t----------")
        # orifice link information

        self.write_weirs = SectionWriterAsListOf("[WEIRS]", Weir, SectionWriter,
            ";;Name          \tFrom Node       \tTo Node         \tType        \tCrestHt   \tQcoeff    \tGated   \tEndCon  \tEndCoeff  \tSurcharge \tRoadWidth \tRoadSurf\n"
            ";;--------------\t----------------\t----------------\t------------\t----------\t----------\t--------\t--------\t----------\t----------\t----------\t----------")
        # weir link information

        self.write_outlets = SectionWriterAsListOf("[OUTLETS]", Outlet, SectionWriter,
            ";;Name          \tFrom Node       \tTo Node         \tOffset    \tType           \tQTable/Qcoeff   \tQexpon    \tGated\n"
            ";;--------------\t----------------\t----------------\t----------\t---------------\t----------------\t----------\t--------")
        # outlet link information

        self.write_xsections = SectionWriterAsListOf("[XSECTIONS]", CrossSection, CrossSectionWriter,
            ";;Link          \tShape       \tGeom1           \tGeom2     \tGeom3     \tGeom4     \tBarrels   \tCulvert   \n"
            ";;--------------\t------------\t----------------\t----------\t----------\t----------\t----------\t----------")
        # conduit, orifice, and weir cross-section geometry

        self.write_transects = TransectsWriter() # TRANSECTS # transect geometry for conduits with irregular cross-sections
        # self.write_losses = [Section] # LOSSES # conduit entrance/exit losses and flap valves
        self.write_controls = SectionWriterAsListOf("[CONTROLS]", basestring, SectionWriter, None)  # rules that control pump and regulator operation
        self.write_landuses = SectionWriterAsListOf("[LANDUSES]", Landuse, LanduseWriter,
                                        ";;              \tSweeping  \tFraction  \tLast\n"
                                        ";;Name          \tInterval  \tAvailable \tSwept\n"
                                        ";;--------------\t----------\t----------\t----------")
        # land use categories

        self.write_buildup = SectionWriterAsListOf("[BUILDUP]", Buildup, BuildupWriter,
            ";;Land Use      \tPollutant       \tFunction  \tCoeff1    \tCoeff2    \tCoeff3    \tPer Unit\n"
            ";;--------------\t----------------\t----------\t----------\t----------\t----------\t----------")
        # buildup functions for pollutants and land uses

        self.write_washoff = SectionWriterAsListOf("[WASHOFF]", Washoff, WashoffWriter,
            ";;Land Use      \tPollutant       \tFunction  \tCoeff1    \tCoeff2    \tSweepRmvl \tBmpRmvl\n"
            ";;--------------\t----------------\t----------\t----------\t----------\t----------\t----------")
        # washoff functions for pollutants and land uses

        self.write_pollutants = SectionWriterAsListOf("[POLLUTANTS]", Pollutant, PollutantWriter,
            ";;Name          \tUnits \tCrain     \tCgw       \tCrdii     \tKdecay    \tSnowOnly  \tCo-Pollutant    \tCo-Frac   \tCdwf      \tCinit\n"
            ";;--------------\t------\t----------\t----------\t----------\t----------\t----------\t----------------\t----------\t----------\t----------")
        # pollutant information

        self.write_coverages = CoveragesWriter() # COVERAGES # assignment of land uses to subcatchments
        self.write_treatment = SectionWriterAsListOf("[TREATMENT]", Treatment, TreatmentWriter,
                                         ";;Node          \tPollutant       \tFunction\n"
                                         ";;--------------\t----------------\t--------")

        # pollutant removal functions at conveyance system nodes

        self.write_inflows = SectionWriterAsListOf("[INFLOWS]", DirectInflow, DirectInflowWriter,
            ";;Node          \tConstituent     \tTime Series     \tType    \tMfactor \tSfactor \tBaseline\tPattern\n"
            ";;--------------\t----------------\t----------------\t--------\t--------\t--------\t--------\t--------")
        # INFLOWS # external hydrograph/pollutograph inflow at nodes

        self.write_dwf = SectionWriterAsListOf("[DWF]", DryWeatherInflow, DryWeatherInflowWriter,
                                   ";;Node          \tConstituent     \tBaseline  \tPatterns  \n"
                                   ";;--------------\t----------------\t----------\t----------")
        # baseline dry weather sanitary inflow at nodes

        self.write_patterns = SectionWriterAsListOf("[PATTERNS]", Pattern, PatternWriter,
                                               ";;Name          \tType      \tMultipliers\n"
                                               ";;--------------\t----------\t-----------")
        # PATTERNS      periodic variation in dry weather inflow

        self.write_rdii = SectionWriterAsListOf("[RDII]", RDIInflow, RDIInflowWriter,
                                    ";;Node          \tUnit Hydrograph \tSewer Area\n"
                                    ";;--------------\t----------------\t----------")
        # rainfall-dependent I/I information at nodes

        self.write_loadings = InitialLoadingsWriter()
        # initial pollutant loads on subcatchments

        self.write_curves = SectionWriterAsListOf("[CURVES]", Curve, CurveWriter,
                                             ";;Name          \tType      \tX-Value   \tY-Value   \n"
                                             ";;--------------\t----------\t----------\t----------")
        # CURVES        x-y tabular data referenced in other sections

        self.write_timeseries = SectionWriterAsListOf("[TIMESERIES]", TimeSeries, TimeSeriesWriter,
                                                 ";;Name          \tDate      \tTime      \tValue\n"
                                                 ";;--------------\t----------\t----------\t----------")
        # time series data referenced in other sections

        # self.write_labels = SectionWriterAsListGroupByID("[LABELS]", Label, LabelWriter,
        #                                          ";;X-Coord         \tY-Coord           \tLabel\n")
        # X,Y coordinates and text of labels

        self.write_polygons = SectionWriterAsListOf("[POLYGONS]", Coordinate, CoordinateWriter,
                                                    ";Subbasin        \tX-Coord         \tY-Coord")
        # X, Y coordinates for each vertex of subcatchment polygons

        self.write_coordinates = SectionWriterAsListOf("[COORDINATES]", Coordinate, CoordinateWriter,
                                                       ";Node            \tX-Coord         \tY-Coord")
        # X, Y coordinates for nodes

        # self.write_vertices = [Section] # VERTICES # X,Y coordinates for each interior vertex of polyline links
        # self.write_symbols = [Section] # SYMBOLS # X,Y coordinates for rain gages
        #  X,Y coordinates of the bounding rectangle and file name of the backdrop image.
        # [TAGS]

    def as_text(self, project):
        # Figure out which kind of infiltration will be written for this project
        infiltration = project.options.infiltration.upper()
        if infiltration == "HORTON":
            self.write_infiltration = SectionWriterAsListOf(
                "[INFILTRATION]", HortonInfiltration, HortonInfiltrationWriter,
                ";;Subcatchment  \tMaxRate   \tMinRate   \tDecay     \tDryTime   \tMaxInfiltration\n"
                ";;--------------\t----------\t----------\t----------\t----------\t----------")
        elif infiltration.startswith("GREEN"):
            self.write_infiltration = SectionWriterAsListOf(
                "[INFILTRATION]", GreenAmptInfiltration, GreenAmptInfiltrationWriter,
                ";;Subcatchment  \tSuction   \tKsat      \tIMD       \n"
                ";;--------------\t----------\t----------\t----------")
        elif infiltration.startswith("CURVE"):
            self.write_infiltration = SectionWriterAsListOf(
                "[INFILTRATION]", CurveNumberInfiltration, CurveNumberInfiltrationWriter,
                ";;Subcatchment  \tCurveNum  \t          \tDryTime   \n"
                ";;--------------\t----------\t----------\t----------")
        subareas = SectionAsListOf("[SUBAREAS]", Subcatchment)
        subareas.value = project.subcatchments.value
        return InputFileWriterBase.as_text(self, project) + '\n' + self.write_subareas.as_text(subareas)
