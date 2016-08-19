from core.inp_writer_base import InputFileWriterBase, SectionWriterAsList, SectionAsList
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
        self.write_raingages = SectionWriterAsList("[RAINGAGES]", RainGageWriter,
             ";;Name          \tFormat   \tInterval\tSCF     \tSource    \n"
             ";;--------------\t---------\t--------\t--------\t----------")

        self.write_hydrographs = SectionWriterAsList("[HYDROGRAPHS]", UnitHydrographWriter,
            ";;Hydrograph    \tRain Gage/Month \tResponse\tR       \tT       \tK       \tDmax    \tDrecov  \tDinit   \n"
            ";;--------------\t----------------\t--------\t--------\t--------\t--------\t--------\t--------\t--------")
        # unit hydrograph data used to construct RDII inflows

        self.write_evaporation = EvaporationWriter()        # EVAPORATION   evaporation data
        self.write_temperature = TemperatureWriter()        # TEMPERATURE   air temperature and snow melt data
        self.write_adjustments = AdjustmentsWriter()        # ADJUSTMENTS   monthly climate adjustments
        self.write_subcatchments = SectionWriterAsList("[SUBCATCHMENTS]", SubcatchmentWriter,
            ";;Name          \tRain Gage       \tOutlet          \tArea    \t%Imperv \tWidth   \t%Slope  \tCurbLen \tSnowPack        \n"
            ";;--------------\t----------------\t----------------\t--------\t--------\t--------\t--------\t--------\t----------------")
        # basic subcatchment information

        self.write_subareas = SectionWriterAsList("[SUBAREAS]", SubareaWriter,
            ";;Subcatchment  \tN-Imperv  \tN-Perv    \tS-Imperv  \tS-Perv    \tPctZero   \tRouteTo   \tPctRouted\n"
            ";;--------------\t----------\t------------\t--------\t----------\t----------\t----------\t---------")
        # subcatchment impervious/pervious sub-area data

        #self.write_infiltration = SectionWriterAsListOf("[INFILTRATION]", SectionWriter, None)
        # write_infiltration is set in as_text based on the kind of infiltration being used in the project.

        self.write_lid_controls = SectionWriterAsList("[LID_CONTROLS]", LIDControlWriter,
                                                   ";;Name          \tType/Layer\tParameters\n"
                                                   ";;--------------\t----------\t----------")
        # low impact development control information

        self.write_lid_usage = SectionWriterAsList("[LID_USAGE]", LIDUsageWriter,
            ";;Subcatchment  \tLID Process     \tNumber \tArea      \tWidth     \tInitSat   \tFromImp   \tToPerv    \tRptFile                 \tDrainTo\n"
            ";;--------------\t----------------\t-------\t----------\t----------\t----------\t----------\t----------\t------------------------\t----------------")
        # assignment of LID controls to subcatchments

        self.write_aquifers = SectionWriterAsList("[AQUIFERS]", AquiferWriter,
            ";;Aquifer       \tPhi   \tWP    \tFC    \tHydCon\tKslope\tTslope\tUEF   \tLED   \tLGLR  \tBEL   \tWTEL  \tUZM   \tUEF Pat\n"
            ";;--------------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t-------")
        # groundwater aquifer parameters

        self.write_groundwater = SectionWriterAsList("[GROUNDWATER]", GroundwaterWriter,
            ";;Subcatchment  \tAquifer         \tNode            \tEsurf \tA1    \tB1    \tA2    \tB2    \tA3    \tDsw   \tEgwt  \tEbot  \tWgr   \tUmc   \n"
            ";;--------------\t----------------\t----------------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t------\t------")
        # subcatchment groundwater parameters

        self.write_snowpacks = SectionWriterAsList("[SNOWPACKS]", SnowPackWriter,
                                                ";;Name          \tSurface   \tParameters\n"
                                                ";;--------------\t----------\t----------")
        # subcatchment snow pack parameters

        self.write_junctions = SectionWriterAsList("[JUNCTIONS]", JunctionWriter,
                                         ";;Name          \tElevation \tMaxDepth  \tInitDepth \tSurDepth  \tAponded\n"
                                         ";;--------------\t----------\t----------\t----------\t----------\t----------")
        # junction node information

        self.write_outfalls = SectionWriterAsList("[OUTFALLS]", OutfallWriter,
                              ";;Name          \tElevation \tType      \tStage Data      \tGated   \tRoute To\n"
                              ";;--------------\t----------\t----------\t----------------\t--------\t----------------")
        #  outfall node information

        self.write_dividers = SectionWriterAsList("[DIVIDERS]", DividerWriter,
                                         ";;Name          \tElevation \tDiverted Link   \tType      \tParameters\n"
                                         ";;--------------\t----------\t----------------\t----------\t----------")
        #  flow divider node information

        self.write_storage = SectionWriterAsList("[STORAGE]", SectionWriter,
                                         ";;Name          \tElev.   \tMaxDepth  \tInitDepth  \tShape     \tCurve Name/Params           \tN/A     \tFevap   \tPsi     \tKsat    \tIMD\n"
                                         ";;--------------\t--------\t----------\t-----------\t----------\t----------------------------\t--------\t--------\t--------\t--------\t--------")
        #  storage node information

        self.write_conduits = SectionWriterAsList("[CONDUITS]", ConduitWriter,
            ";;Name          \tFrom Node       \tTo Node         \tLength    \tRoughness \tInOffset  \tOutOffset \tInitFlow  \tMaxFlow\n"
            ";;--------------\t----------------\t----------------\t----------\t----------\t----------\t----------\t----------\t----------")
        # conduit link information

        self.write_pumps = SectionWriterAsList("[PUMPS]", PumpWriter,
            ";;Name          \tFrom Node       \tTo Node         \tPump Curve      \tStatus  \tStartup \tShutoffn"
            ";;--------------\t----------------\t----------------\t----------------\t--------\t--------\t--------")
        # pump link information

        self.write_orifices = SectionWriterAsList("[ORIFICES]", OrificeWriter,
            ";;Name          \tFrom Node       \tTo Node         \tType        \tOffset    \tQcoeff    \tGated   \tCloseTime\n"
            ";;--------------\t----------------\t----------------\t------------\t----------\t----------\t--------\t----------")
        # orifice link information

        self.write_weirs = SectionWriterAsList("[WEIRS]", WeirWriter,
            ";;Name          \tFrom Node       \tTo Node         \tType        \tCrestHt   \tQcoeff    \tGated   \tEndCon  \tEndCoeff  \tSurcharge \tRoadWidth \tRoadSurf\n"
            ";;--------------\t----------------\t----------------\t------------\t----------\t----------\t--------\t--------\t----------\t----------\t----------\t----------")
        # weir link information

        self.write_outlets = SectionWriterAsList("[OUTLETS]", SectionWriter,
            ";;Name          \tFrom Node       \tTo Node         \tOffset    \tType           \tQTable/Qcoeff   \tQexpon    \tGated\n"
            ";;--------------\t----------------\t----------------\t----------\t---------------\t----------------\t----------\t--------")
        # outlet link information

        self.write_xsections = SectionWriterAsList("[XSECTIONS]", CrossSectionWriter,
            ";;Link          \tShape       \tGeom1           \tGeom2     \tGeom3     \tGeom4     \tBarrels   \tCulvert   \n"
            ";;--------------\t------------\t----------------\t----------\t----------\t----------\t----------\t----------")
        # conduit, orifice, and weir cross-section geometry

        self.write_transects = TransectsWriter()  # transect geometry for conduits with irregular cross-sections

        self.write_losses = SectionWriterAsList("[LOSSES]", LossWriter,
            ";;Link          \tKentry    \tKexit     \tKavg      \tFlap Gate \tSeepage   \n"
            ";;--------------\t----------\t----------\t----------\t----------\t----------")
        # conduit entrance/exit losses and flap valves

        self.write_controls = SectionWriterAsList("[CONTROLS]", SectionWriter, None)  # rules that control pump and regulator operation
        self.write_landuses = SectionWriterAsList("[LANDUSES]", LanduseWriter,
                                                  ";;              \tSweeping  \tFraction  \tLast\n"
                                                  ";;Name          \tInterval  \tAvailable \tSwept\n"
                                                  ";;--------------\t----------\t----------\t----------")
        # land use categories

        self.write_buildup = SectionWriterAsList("[BUILDUP]", BuildupWriter,
            ";;Land Use      \tPollutant       \tFunction  \tCoeff1    \tCoeff2    \tCoeff3    \tPer Unit\n"
            ";;--------------\t----------------\t----------\t----------\t----------\t----------\t----------")
        # buildup functions for pollutants and land uses

        self.write_washoff = SectionWriterAsList("[WASHOFF]", WashoffWriter,
            ";;Land Use      \tPollutant       \tFunction  \tCoeff1    \tCoeff2    \tSweepRmvl \tBmpRmvl\n"
            ";;--------------\t----------------\t----------\t----------\t----------\t----------\t----------")
        # washoff functions for pollutants and land uses

        self.write_pollutants = SectionWriterAsList("[POLLUTANTS]", PollutantWriter,
            ";;Name          \tUnits \tCrain     \tCgw       \tCrdii     \tKdecay    \tSnowOnly  \tCo-Pollutant    \tCo-Frac   \tCdwf      \tCinit\n"
            ";;--------------\t------\t----------\t----------\t----------\t----------\t----------\t----------------\t----------\t----------\t----------")
        # pollutant information

        self.write_coverages = CoveragesWriter() # COVERAGES # assignment of land uses to subcatchments
        self.write_treatment = SectionWriterAsList("[TREATMENT]", TreatmentWriter,
                                                   ";;Node          \tPollutant       \tFunction\n"
                                                   ";;--------------\t----------------\t--------")
        # pollutant removal functions at conveyance system nodes

        self.write_inflows = SectionWriterAsList("[INFLOWS]", DirectInflowWriter,
            ";;Node          \tConstituent     \tTime Series     \tType    \tMfactor \tSfactor \tBaseline\tPattern\n"
            ";;--------------\t----------------\t----------------\t--------\t--------\t--------\t--------\t--------")
        # INFLOWS # external hydrograph/pollutograph inflow at nodes

        self.write_dwf = SectionWriterAsList("[DWF]", DryWeatherInflowWriter,
                                   ";;Node          \tConstituent     \tBaseline  \tPatterns  \n"
                                   ";;--------------\t----------------\t----------\t----------")
        # baseline dry weather sanitary inflow at nodes

        self.write_patterns = SectionWriterAsList("[PATTERNS]", PatternWriter,
                                               ";;Name          \tType      \tMultipliers\n"
                                               ";;--------------\t----------\t-----------")
        # PATTERNS      periodic variation in dry weather inflow

        self.write_rdii = SectionWriterAsList("[RDII]", RDIInflowWriter,
                                    ";;Node          \tUnit Hydrograph \tSewer Area\n"
                                    ";;--------------\t----------------\t----------")
        # rainfall-dependent I/I information at nodes

        self.write_loadings = InitialLoadingsWriter()
        # initial pollutant loads on subcatchments

        self.write_curves = SectionWriterAsList("[CURVES]", CurveWriter,
                                                ";;Name          \tType      \tX-Value   \tY-Value   \n"
                                                ";;--------------\t----------\t----------\t----------")
        # CURVES        x-y tabular data referenced in other sections

        self.write_timeseries = SectionWriterAsList("[TIMESERIES]", TimeSeriesWriter,
                                                    ";;Name          \tDate      \tTime      \tValue\n"
                                                    ";;--------------\t----------\t----------\t----------")
        # time series data referenced in other sections

        self.write_labels = SectionWriterAsList("[LABELS]", LabelWriter,
                                                ";;X-Coord         \tY-Coord           \tLabel")
        # X, Y coordinates, text, and font details of labels

        self.write_polygons = SectionWriterAsList("[POLYGONS]", CoordinateWriter,
                                                  ";Subcatchment    \tX-Coord   \tY-Coord")
        # X, Y coordinates for each vertex of subcatchment polygons

        self.write_coordinates = SectionWriterAsList("[COORDINATES]", CoordinateWriter,
                                                     ";Node            \tX-Coord   \tY-Coord")
        # X, Y coordinates for nodes

        self.write_vertices = SectionWriterAsList("[VERTICES]", CoordinateWriter,
                                                  ";Link            \tX-Coord   \tY-Coord")
        # self.write_vertices = [Section] # VERTICES # X,Y coordinates for each interior vertex of polyline links
        self.write_symbols = SectionWriterAsList("[SYMBOLS]", CoordinateWriter,
                                                 ";Gage            \tX-Coord   \tY-Coord")
        # X, Y coordinates for rain gages
        #  X,Y coordinates of the bounding rectangle and file name of the backdrop image.

        self.write_tags = TagsWriter()
        # [TAGS]

    def as_text(self, project):
        # Figure out which kind of infiltration will be written for this project
        infiltration = project.options.infiltration.upper()
        if infiltration == "HORTON":
            self.write_infiltration = SectionWriterAsList(
                "[INFILTRATION]", HortonInfiltrationWriter,
                ";;Subcatchment  \tMaxRate   \tMinRate   \tDecay     \tDryTime   \tMaxInfiltration\n"
                ";;--------------\t----------\t----------\t----------\t----------\t----------")
        elif infiltration.startswith("GREEN"):
            self.write_infiltration = SectionWriterAsList(
                "[INFILTRATION]", GreenAmptInfiltrationWriter,
                ";;Subcatchment  \tSuction   \tKsat      \tIMD       \n"
                ";;--------------\t----------\t----------\t----------")
        elif infiltration.startswith("CURVE"):
            self.write_infiltration = SectionWriterAsList(
                "[INFILTRATION]", CurveNumberInfiltrationWriter,
                ";;Subcatchment  \tCurveNum  \t          \tDryTime   \n"
                ";;--------------\t----------\t----------\t----------")

        inp = InputFileWriterBase.as_text(self, project)

        subareas = SectionAsList("[SUBAREAS]")  # (list of Subcatchment)
        subareas.value = project.subcatchments.value
        subareas_text = self.write_subareas.as_text(subareas)
        if subareas_text:
            inp += '\n' + subareas_text + '\n'

        tags_text = self.write_tags.as_text(project)
        if tags_text:
            inp += '\n' + tags_text + '\n'

        losses = SectionAsList("[LOSSES]")  # (list of Conduit)
        losses.value = project.conduits.value
        losses_text = self.write_losses.as_text(losses)
        if losses_text:
            inp += '\n' + losses_text + '\n'

        return inp
