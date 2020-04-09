from core.inp_reader_base import InputFileReader, SectionReaderAsList, SectionReaderAsListGroupByID
# from core.swmm.hydraulics.control import ControlRule
from core.swmm.hydraulics.node import Junction, Outfall, Divider, StorageUnit
from core.swmm.hydraulics.node import DirectInflow, DryWeatherInflow, RDIInflow, Treatment
from core.swmm.hydraulics.link import Conduit, Pump, Orifice, Weir, Outlet, CrossSection, Transects
from core.swmm.title import Title
from core.swmm.options.general import General, flow_units_metric
# from core.swmm.options.time_steps import TimeSteps
from core.swmm.options.report import Report
from core.swmm.options.files import Files
from core.swmm.options.backdrop import BackdropOptions
from core.swmm.options.map import MapOptions
from core.swmm.options.events import Events
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

try:  # maintain compatibility with both python 2 and 3
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str


class ProjectReader(InputFileReader):
    """Read a SWMM input file into in-memory data structures"""

    def __init__(self):
        """Define the fields of a SWMM Project by creating an empty placeholder for each section"""

        self.read_title = TitleReader()               # TITLE         project title
        self.read_options = GeneralReader()           # OPTIONS       analysis options
        self.read_report = ReportReader()             # REPORT        output reporting instructions
        self.read_files = SectionReader()             # FILES         interface file options
        self.read_files.SECTION_NAME = "[FILES]"
        self.read_files.section_type = Files
        self.read_backdrop = BackdropOptionsReader()  # BACKDROP      bounding rectangle and file name of backdrop image
        self.read_map = MapOptionsReader()            # MAP           map's bounding rectangle and units
        self.read_raingages = SectionReaderAsList("[RAINGAGES]", RainGageReader)

        self.read_hydrographs = SectionReaderAsListGroupByID("[HYDROGRAPHS]", UnitHydrographReader)
        # unit hydrograph data used to construct RDII inflows

        self.read_evaporation = EvaporationReader()   # EVAPORATION   evaporation data
        self.read_temperature = TemperatureReader()   # TEMPERATURE   air temperature and snow melt data
        self.read_adjustments = AdjustmentsReader()   # ADJUSTMENTS   monthly climate adjustments
        self.read_subcatchments = SectionReaderAsList("[SUBCATCHMENTS]", SubcatchmentReader)
        # basic subcatchment information

        self.read_infiltration = SectionReaderAsList("[INFILTRATION]", None)
        # This is set to SectionReaderAsListOf HortonInfiltration or GreenAmptInfiltration or CurveNumberInfiltration
        # below in read_section based on subcatchment infiltration parameters

        self.read_lid_controls = SectionReaderAsListGroupByID("[LID_CONTROLS]", LIDControlReader)
        # low impact development control information

        self.read_lid_usage = SectionReaderAsList("[LID_USAGE]", LIDUsageReader)
        # assignment of LID controls to subcatchments

        self.read_aquifers = SectionReaderAsList("[AQUIFERS]", AquiferReader)
        # groundwater aquifer parameters

        self.read_groundwater = SectionReaderAsList("[GROUNDWATER]", GroundwaterReader)
        # subcatchment groundwater parameters

        self.read_gwf = SectionReaderAsList("[GWF]", GWFReader)
        # subcatchment groundwater flow equations

        self.read_snowpacks = SectionReaderAsListGroupByID("[SNOWPACKS]", SnowPackReader)
        # subcatchment snow pack parameters

        self.read_junctions = SectionReaderAsList("[JUNCTIONS]", JunctionReader)
        # junction node information

        self.read_outfalls = SectionReaderAsList("[OUTFALLS]", OutfallReader)
        #  outfall node information

        self.read_dividers = SectionReaderAsList("[DIVIDERS]", DividerReader)
        #  flow divider node information

        self.read_storage = SectionReaderAsList("[STORAGE]", StorageReader)
        #  storage node information

        self.read_conduits = SectionReaderAsList("[CONDUITS]", ConduitReader)
        # conduit link information

        self.read_pumps = SectionReaderAsList("[PUMPS]", PumpReader)
        # pump link information

        self.read_orifices = SectionReaderAsList("[ORIFICES]", OrificeReader)
        # orifice link information

        self.read_weirs = SectionReaderAsList("[WEIRS]", WeirReader)
        # weir link information

        self.read_outlets = SectionReaderAsList("[OUTLETS]", OutletReader)
        # outlet link information

        self.read_xsections = SectionReaderAsList("[XSECTIONS]", CrossSectionReader)
        # conduit, orifice, and weir cross-section geometry

        self.read_transects = TransectsReader()
        # transect geometry for conduits with irregular cross-sections

        self.read_controls = ControlsReader()
        # rules that control pump and regulator operation

        self.read_events = SectionReaderAsList("[EVENTS]", EventsReader)
        # events

        self.read_landuses = SectionReaderAsList("[LANDUSES]", LanduseReader)
        # land use categories

        self.read_buildup = SectionReaderAsList("[BUILDUP]", BuildupReader)
        # buildup functions for pollutants and land uses

        self.read_washoff = SectionReaderAsList("[WASHOFF]", WashoffReader)
        # washoff functions for pollutants and land uses

        self.read_pollutants = SectionReaderAsList("[POLLUTANTS]", PollutantReader)
        # pollutant information

        self.read_coverages = CoveragesReader() # COVERAGES # assignment of land uses to subcatchments
        self.read_treatment = SectionReaderAsList("[TREATMENT]", TreatmentReader)

        # pollutant removal functions at conveyance system nodes

        self.read_inflows = SectionReaderAsList("[INFLOWS]", DirectInflowReader)
        # INFLOWS # external hydrograph/pollutograph inflow at nodes

        self.read_dwf = SectionReaderAsList("[DWF]", DryWeatherInflowReader)
        # baseline dry weather sanitary inflow at nodes

        self.read_patterns = SectionReaderAsListGroupByID("[PATTERNS]", PatternReader)
        # PATTERNS      periodic variation in dry weather inflow

        self.read_rdii = SectionReaderAsList("[RDII]", RDIInflowReader)
        # rainfall-dependent I/I information at nodes

        self.read_loadings = InitialLoadingsReader()
        # initial pollutant loads on subcatchments

        self.read_curves = SectionReaderAsListGroupByID("[CURVES]", CurveReader)
        # CURVES        x-y tabular data referenced in other sections

        self.read_timeseries = SectionReaderAsListGroupByID("[TIMESERIES]", TimeSeriesReader)
        # time series data referenced in other sections

        self.read_labels = SectionReaderAsList("[LABELS]", LabelReader)
        # X, Y coordinates, text, and font details of labels

        # temporary storage for sections that need to be read after other sections
        self.defer_subareas = None
        self.defer_coordinates = None
        self.defer_symbols = None
        self.defer_tags = None
        self.defer_losses = None
        self.defer_vertices = None
        self.defer_polygons = None

    def read_section(self, project, section_name, section_text):
        section_name_upper = section_name.upper()
        if section_name_upper == project.infiltration.SECTION_NAME.upper():
            # self.check_valid_subcatchment_id(project, 'INFILTRATION', section_text)
            infiltration = project.options.infiltration.upper()
            if infiltration.startswith("HORTON") or infiltration.startswith("MODIFIED_HORTON"):
                self.read_infiltration = SectionReaderAsList(section_name, HortonInfiltrationReader)
            elif infiltration.startswith("GREEN") or infiltration.startswith("MODIFIED_GREEN"):
                self.read_infiltration = SectionReaderAsList(section_name, GreenAmptInfiltrationReader)
            elif infiltration.startswith("CURVE"):
                self.read_infiltration = SectionReaderAsList(section_name, CurveNumberInfiltrationReader)
        elif section_name_upper == "[SUBAREAS]":
            # self.check_valid_subcatchment_id(project, 'SUBAREAS', section_text)
            self.defer_subareas = section_text
            return  # Skip read_section, defer until finished_reading is called.
        elif section_name_upper == "[COORDINATES]":
            # self.check_valid_node_id(project, 'COORDINATES', section_text)
            self.defer_coordinates = section_text
            return  # Skip read_section, defer until finished_reading is called.
        elif section_name_upper == "[SYMBOLS]":
            # self.check_valid_raingage_id(project, 'SYMBOLS', section_text)
            self.defer_symbols = section_text
            return  # Skip read_section, defer until finished_reading is called.
        elif section_name_upper == "[TAGS]":
            self.defer_tags = section_text
            return  # Skip read_section, defer until finished_reading is called.
        elif section_name_upper == "[LOSSES]":
            # self.check_valid_link_id(project, 'LOSSES', section_text)
            self.defer_losses = section_text
            return
        elif section_name_upper == "[VERTICES]":
            # self.check_valid_link_id(project, 'VERTICES', section_text)
            self.defer_vertices = section_text
            return
        elif section_name_upper == "[POLYGONS]":
            # self.check_valid_subcatchment_id(project, 'POLYGONS', section_text)
            self.defer_polygons = section_text
            return
        elif section_name_upper == "[GROUNDWATER]":
            # self.check_valid_subcatchment_id(project, 'GROUNDWATER', section_text)
            pass
        elif section_name_upper == "[GWF]":
            # self.check_valid_subcatchment_id(project, 'GWF', section_text)
            pass
        elif section_name_upper == "[COVERAGES]":
            # self.check_valid_subcatchment_id(project, 'COVERAGES', section_text)
            # self.check_valid_landuse_id(project, 'COVERAGES', section_text)
            pass
        elif section_name_upper == "[LOADINGS]":
            # self.check_valid_subcatchment_id(project, 'LOADINGS', section_text)
            pass
        elif section_name_upper == "[LID_USAGE]":
            # self.check_valid_subcatchment_id(project, 'LID_USAGE', section_text)
            # self.check_valid_lid_id(project, 'LID_USAGE', section_text)
            pass
        elif section_name_upper == "[CONDUITS]":
            # self.check_valid_node_id(project, 'CONDUITS', section_text)
            pass
        elif section_name_upper == "[PUMPS]":
            # self.check_valid_node_id(project, 'PUMPS', section_text)
            pass
        elif section_name_upper == "[ORIFICES]":
            # self.check_valid_node_id(project, 'ORIFICES', section_text)
            pass
        elif section_name_upper == "[WEIRS]":
            # self.check_valid_node_id(project, 'WEIRS', section_text)
            pass
        elif section_name_upper == "[OUTLETS]":
            # self.check_valid_node_id(project, 'OUTLETS', section_text)
            pass
        elif section_name_upper == "[TREATMENT]":
            # self.check_valid_node_id(project, 'TREATMENT', section_text)
            # self.check_valid_pollutant_id(project, 'TREATMENT', section_text)
            pass
        elif section_name_upper == "[INFLOWS]":
            # self.check_valid_node_id(project, 'INFLOWS', section_text)
            # self.check_valid_pollutant_id(project, 'INFLOWS', section_text)
            pass
        elif section_name_upper == "[DWF]":
            # self.check_valid_node_id(project, 'DWF', section_text)
            pass
        elif section_name_upper == "[RDII]":
            # self.check_valid_node_id(project, 'RDII', section_text)
            pass
        elif section_name_upper == "[XSECTIONS]":
            # self.check_valid_link_id(project, 'XSECTIONS', section_text)
            pass
        elif section_name_upper == "[LOSSES]":
            # self.check_valid_link_id(project, 'LOSSES', section_text)
            pass
        elif section_name_upper == "[BUILDUP]":
            # self.check_valid_landuse_id(project, 'BUILDUP', section_text)
            # self.check_valid_pollutant_id(project, 'BUILDUP', section_text)
            pass
        elif section_name_upper == "[WASHOFF]":
            # self.check_valid_landuse_id(project, 'WASHOFF', section_text)
            # self.check_valid_pollutant_id(project, 'WASHOFF', section_text)
            pass
        elif section_name_upper == "[SUBCATCHMENTS]":
            # self.check_valid_raingage_id(project, 'SUBCATCHMENTS', section_text)
            pass
        InputFileReader.read_section(self, project, section_name, section_text)

    def finished_reading(self, project):
        if self.defer_subareas:
            # self.check_valid_subcatchment_id(project, 'SUBAREAS', self.defer_subareas)
            SubareasReader.read(self.defer_subareas, project)
            self.defer_subareas = None
        if self.defer_coordinates:
            # self.check_valid_node_id(project, 'COORDINATES', self.defer_coordinates)
            CoordinatesReader.read(self.defer_coordinates, project)
            self.defer_coordinates = None
        if self.defer_symbols:
            # self.check_valid_raingage_id(project, 'SYMBOLS', self.defer_symbols)
            SymbolsReader.read(self.defer_symbols, project)
            self.defer_symbols = None
        if self.defer_tags:
            TagsReader.read(self.defer_tags, project)
            self.defer_tags = None
        if self.defer_losses:
            # self.check_valid_link_id(project, 'LOSSES', self.defer_losses)
            LossesReader.read(self.defer_losses, project)
            self.defer_losses = None
        if self.defer_vertices:
            # self.check_valid_link_id(project, 'VERTICES', self.defer_vertices)
            VerticesReader.read(self.defer_vertices, project)
            self.defer_vertices = None
        if self.defer_polygons:
            # self.check_valid_subcatchment_id(project, 'POLYGONS', self.defer_polygons)
            PolygonsReader.read(self.defer_polygons, project)
            self.defer_polygons = None
        project.metric = project.options.flow_units in flow_units_metric
        project.set_pattern_object_references()

    def check_valid_subcatchment_id(self, project, section_name, section_text):
        # check for valid subcatchment ids
        temp_text = section_text
        try:
            for line in temp_text.splitlines():
                if line[0:1] == '[' or line[0:1] == ';':
                    pass
                else:
                    fields = line.split()
                    if len(fields) > 0:
                        if "none" in fields[0].lower():
                            pass
                        subcatchment_name = fields[0]
                        found = False
                        try:
                            if project.subcatchments.value[subcatchment_name]:
                                found = True
                        except KeyError as ke:
                            pass
                        if not found:
                            self.input_err_msg += '\n' + 'Undefined Subcatchment (' + subcatchment_name + ') referenced in ' + section_name + ' section.'
        except:
            pass


    def check_valid_node_id(self, project, section_name, section_text):
        # check for valid node ids
        temp_text = section_text
        try:
            for line in temp_text.splitlines():
                if line[0:1] == '[' or line[0:1] == ';':
                    pass
                else:
                    fields = line.split()
                    if len(fields) > 0:
                        if "none" in fields[0].lower():
                            pass
                        if section_name == "CONDUITS" or section_name == "PUMPS" or section_name == "ORIFICES" or section_name == "WEIRS" or section_name == "OUTLETS":
                            node_name = fields[1]
                            found = False
                            for node in project.all_nodes():
                                if node.name == node_name:
                                    found = True
                            if not found:
                                self.input_err_msg += '\n' + 'Undefined Node (' + node_name + ') referenced in ' + section_name + ' section.'
                            node_name = fields[2]
                            found = False
                            for node in project.all_nodes():
                                if node.name == node_name:
                                    found = True
                            if not found:
                                self.input_err_msg += '\n' + 'Undefined Node (' + node_name + ') referenced in ' + section_name + ' section.'
                        else:
                            node_name = fields[0]
                            found = False
                            for node in project.all_nodes():
                                if node.name == node_name:
                                    found = True
                            if not found:
                                self.input_err_msg += '\n' + 'Undefined Node (' + node_name + ') referenced in ' + section_name + ' section.'
        except:
            pass


    def check_valid_link_id(self, project, section_name, section_text):
        # check for valid link ids
        temp_text = section_text
        try:
            for line in temp_text.splitlines():
                if line[0:1] == '[' or line[0:1] == ';':
                    pass
                else:
                    fields = line.split()
                    if len(fields) > 0:
                        if "none" in fields[0].lower():
                            pass
                        link_name = fields[0]
                        found = False
                        for link in project.all_links():
                            if link.name == link_name:
                                found = True
                        if not found:
                            self.input_err_msg += '\n' + 'Undefined Link (' + link_name + ') referenced in ' + section_name + ' section.'
        except:
            pass


    def check_valid_landuse_id(self, project, section_name, section_text):
        # check for valid landuse ids
        temp_text = section_text
        try:
            for line in temp_text.splitlines():
                if line[0:1] == '[' or line[0:1] == ';':
                    pass
                else:
                    fields = line.split()
                    if len(fields) > 0:
                        if "none" in fields[0].lower():
                            pass
                        landuse_name = fields[0]
                        if section_name == 'COVERAGES':
                            landuse_name = fields[1]
                        found = False
                        for landuse in project.landuses.value:
                            if landuse.name == landuse_name:
                                found = True
                        if not found:
                            self.input_err_msg += '\n' + 'Undefined Land Use (' + landuse_name + ') referenced in ' + section_name + ' section.'
        except:
            pass


    def check_valid_pollutant_id(self, project, section_name, section_text):
        # check for valid pollutant ids
        temp_text = section_text
        try:
            for line in temp_text.splitlines():
                if line[0:1] == '[' or line[0:1] == ';':
                    pass
                else:
                    fields = line.split()
                    if len(fields) > 1:
                        if "none" in fields[0].lower():
                            pass
                        pollutant_name = fields[1]
                        found = False
                        if pollutant_name == "FLOW" or pollutant_name.upper() == "FLOW":
                            found = True
                        for pollutant in project.pollutants.value:
                            if pollutant.name == pollutant_name:
                                found = True
                        if not found:
                            self.input_err_msg += '\n' + 'Undefined Pollutant (' + pollutant_name + ') referenced in ' + section_name + ' section.'
        except:
            pass


    def check_valid_lid_id(self, project, section_name, section_text):
        # check for valid lid ids
        temp_text = section_text
        try:
            for line in temp_text.splitlines():
                if line[0:1] == '[' or line[0:1] == ';':
                    pass
                else:
                    fields = line.split()
                    if len(fields) > 0:
                        if "none" in fields[0].lower():
                            pass
                        lid_name = fields[1]
                        found = False
                        for lid in project.lid_controls.value:
                            if lid.name == lid_name:
                                found = True
                        if not found:
                            self.input_err_msg += '\n' + 'Undefined LID process (' + lid_name + ') referenced in ' + section_name + ' section.'
        except:
            pass


    def check_valid_raingage_id(self, project, section_name, section_text):
        # check for valid raingage ids
        temp_text = section_text
        try:
            for line in temp_text.splitlines():
                if line[0:1] == '[' or line[0:1] == ';':
                    pass
                else:
                    fields = line.split()
                    if len(fields) > 0:
                        if "none" in fields[0].lower():
                            pass
                        raingage_name = fields[0]
                        if section_name == 'SUBCATCHMENTS':
                            raingage_name = fields[1]
                        found = False
                        for raingage in project.raingages.value:
                            if raingage.name == raingage_name:
                                found = True
                        if not found:
                            self.input_err_msg += '\n' + 'Undefined Raingage (' + raingage_name + ') referenced in ' + section_name + ' section.'
        except:
            pass