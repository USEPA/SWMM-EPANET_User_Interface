from enum import Enum
from core.coordinates import Coordinates
from core.inputfile import Section
from core.metadata import Metadata
from core.swmm.hydrology.raingage import RainGage


class Routing(Enum):
    """Routing of runoff between pervious and impervious areas
        IMPERV: runoff from pervious area flows to impervious area,
        PERV: runoff from impervious area flows to pervious area,
        OUTLET: runoff from both areas flows directly to outlet. """
    IMPERV = 1
    PERV = 2
    OUTLET = 3


class Subcatchment:
    """Subcatchment geometry, location, parameters, and time-series data"""

    #    attribute                  label              default   eng, metric, hint
    metadata = Metadata((
        ("name",                    "Name",            "",       '', '', "User-assigned name of subcatchment"),
        ("centroid.X",              "X-Coordinate",    "",       '', '', "X coordinate of subcatchment centroid on map"),
        ("centroid.Y",              "Y-Coordinate",    "",       '', '', "Y coordinate of subcatchment centroid on map"),
        ("description",             "Description",     "",       '', '', "Optional comment or description"),
        ("tag",                     "Tag",             "",       '', '', "Optional category or classification"),
        ("rain_gage",               "Rain Gage",       "*",      '', '', "Rain gage assigned to subcatchment"),
        ("outlet",                  "Outlet",          "*",      '', '', "Name of node or another subcatchment that receives runoff"),
        ("area",                    "Area",            "5",      '', '', "Area of subcatchment"),
        ("width",                   "Width",           "500",    '', '', "Width of overland flow path"),
        ("percent_slope",           "% Slope",         "0.5",    '', '', "Average surface slope"),
        ("percent_impervious",      "% Imperv",        "25",     '', '', "Percent of impervious area"),
        ("n_imperv",                "N-Imperv",        "0.01",   '', '', "Mannings N for impervious area"),
        ("n_perv",                  "N-Perv",          "0.1",    '', '', "Mannings N for pervious area"),
        ("storage_depth_imperv",    "Dstore-Imperv",   "0.05",   '', '', "Depth of depression storage on impervious area"),
        ("storage_depth_perv",      "Dstore-Perv",     "0.05",   '', '', "Depth of depression storage on pervious area"),
        ("percent_zero_impervious", "%Zero-Imperv",    "25",     '', '', "Percent of impervious area with no depression storage"),
        ("subarea_routing",         "Subarea Routing", "OUTLET", '', '', "Choice of internal routing between pervious and impervious sub-areas"),
        ("percent_routed",          "Percent Routed",  "100",    '', '', "Percent of runoff routed between sub-areas"),
        ("infiltration_parameters", "Infiltration",    "HORTON", '', '', "Infiltration parameters (click to edit)"),
        ("groundwater",             "Groundwater",     "NO",     '', '', "Groundwater flow parameters (click to edit)"),
        ("snow_pack",               "Snow Pack",       "",       '', '', "Name of snow pack parameter set (for snow melt analysis only)"),
        ("LIDUsage",                "LID Controls",    "0",      '', '', "LID controls (click to edit)"),
        ("coverages",               "Land Uses",       "0",      '', '', "Assignment of land uses to subcatchment (click to edit)"),
        ("initial_loadings",        "Initial Buildup", "NONE",   '', '', "Initial pollutant buildup on subcatchment (click to edit)"),
        ("curb_length",             "Curb Length",     "0",      '', '', "Curb length (if needed for pollutant buildup functions)")
    ))

    def __init__(self, name):
        self.name = name
        """str: User-assigned Subcatchment name."""

        self.centroid = Coordinates(None, None)
        """Coordinates: Subcatchment's centroid on the Study Area Map.
            If not set, the subcatchment will not appear on the map."""

        self.polygon_vertices = []
        """List[Coordinates]:the Subcatchment's polygon."""

        self.description = ''
        """str: Optional description of the Subcatchment."""

        self.tag = ''
        """Optional label used to categorize or classify the Subcatchment."""

        self.rain_gage = ''
        """str: The RainGage ID associated with the Subcatchment."""

        self.outlet = ''
        """The Node or Subcatchment which receives Subcatchment's runoff."""

        self.area = ''
        """float: Area of the subcatchment (acres or hectares)."""

        self.percent_impervious = ''
        """float: Percent of land area which is impervious."""

        self.width = ''
        """Characteristic width of the overland flow path for sheet flow
            runoff (feet or meters). An initial estimate of the characteristic
            width is given by the subcatchment area divided by the average
            maximum overland flow length. The maximum overland flow
            length is the length of the flow path from the the furthest drainage
            point of the subcatchment before the flow becomes channelized.
            Maximum lengths from several different possible flow paths
            should be averaged. These paths should reflect slow flow, such as
            over pervious surfaces, more than rapid flow over pavement, for
            example. Adjustments should be made to the width parameter to
            produce good fits to measured runoff hydrographs."""

        self.percent_slope = ''
        """float: Average percent slope of the subcatchment."""

        self.n_imperv = ''
        """float: Manning's n for overland flow in impervious part of Subcatchment"""

        self.n_perv = ''
        """Manning's n for overland flow in pervious part of Subcatchment"""

        self.storage_depth_imperv = ''
        """float: Depth of depression storage on the impervious portion of the
            Subcatchment (inches or millimeters) """

        self.storage_depth_perv = ''
        """float: Depth of depression storage on the pervious portion of the
            Subcatchment (inches or millimeters)"""

        self.percent_zero_impervious = ''
        """float: Percent of the impervious area with no depression storage."""

        self.subarea_routing = Routing.OUTLET
        """Routing: Internal routing of runoff between pervious and impervious areas"""

        self.percent_routed = ''
        """float: Percent of runoff routed between subareas"""

        self.infiltration_parameters = HortonInfiltration()
        """infiltration parameters from horton, green-ampt, or scs classes"""

        self.groundwater = ''
        """Groundwater flow parameters for the subcatchment."""

        self.snow_pack = ''
        """Snow pack parameter set (if any) of the subcatchment."""

        self.curb_length = ''
        """ Total length of curbs in the subcatchment (any length units).
            Used only when initial_loadings are normalized to curb length."""


class HortonInfiltration(Section):
    """Horton Infiltration parameters"""

    field_format = "{:16}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)  # set_text will call __init__ without new_text to do the initialization below
        else:
            Section.__init__(self)

            self.subcatchment = ''
            """Subcatchment name"""

            self.max_rate = ''
            """Maximum infiltration rate on Horton curve (in/hr or mm/hr)"""

            self.min_rate = ''
            """Minimum infiltration rate on Horton curve (in/hr or mm/hr)."""

            self.decay = ''
            """Decay rate constant of Horton curve (1/hr)."""

            self.dry_time = ''
            """Time it takes for fully saturated soil to dry (days)."""

            self.max_volume = ''
            """Maximum infiltration volume possible (in or mm)."""

    def get_text(self):
        inp = ''
        if self.comment:
            inp = self.comment + '\n'
        inp += self.field_format.format(self.subcatchment,
                                        self.max_rate,
                                        self.min_rate,
                                        self.decay,
                                        self.dry_time,
                                        self.max_volume)
        return inp

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 0:
            self.subcatchment = fields[0]
        if len(fields) > 1:
            self.max_rate = fields[1]
        if len(fields) > 2:
            self.min_rate = fields[2]
        if len(fields) > 3:
            self.decay = fields[3]
        if len(fields) > 4:
            self.dry_time = fields[4]
        if len(fields) > 5:
            self.max_volume = fields[5]


class GreenAmptInfiltration(Section):
    """Green-Ampt Infiltration parameters"""

    field_format = "{:16}\t{:10}\t{:10}\t{:10}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)  # set_text will call __init__ without new_text to do the initialization below
        else:
            Section.__init__(self)

            self.subcatchment = ''
            """Subcatchment name"""

            self.suction = ''
            """Soil capillary suction (in or mm)."""

            self.hydraulic_conductivity = ''
            """Soil saturated hydraulic conductivity (in/hr or mm/hr)."""

            self.initial_moisture_deficit = ''
            """Initial soil moisture deficit (volume of voids / total volume)."""

    def get_text(self):
        inp = ''
        if self.comment:
            inp = self.comment + '\n'
        inp += self.field_format.format(self.subcatchment,
                                        self.suction,
                                        self.hydraulic_conductivity,
                                        self.initial_moisture_deficit)
        return inp

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 0:
            self.subcatchment = fields[0]
        if len(fields) > 1:
            self.suction = fields[1]
        if len(fields) > 2:
            self.hydraulic_conductivity = fields[2]
        if len(fields) > 3:
            self.initial_moisture_deficit = fields[3]


class CurveNumberInfiltration(Section):
    """Curve Number Infiltration parameters"""

    field_format = "{:16}\t{:10}\t{:10}\t{:10}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)  # set_text will call __init__ without new_text to do the initialization below
        else:
            Section.__init__(self)

            self.subcatchment = ''
            """Subcatchment name"""

            self.curve_number = None
            """SCS Curve Number"""

            self.hydraulic_conductivity = ''
            """Soil saturated hydraulic conductivity (no longer used for curve number infiltration)."""

            self.dry_days = ''
            """Time it takes for fully saturated soil to dry (days)."""

    def get_text(self):
        inp = ''
        if self.comment:
            inp = self.comment + '\n'
        inp += self.field_format.format(self.subcatchment,
                                        self.curve_number,
                                        self.hydraulic_conductivity,
                                        self.dry_days)
        return inp

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 0:
            self.subcatchment = fields[0]
        if len(fields) > 1:
            self.curve_number = fields[1]
        if len(fields) > 2:
            self.hydraulic_conductivity = fields[2]
        if len(fields) > 3:
            self.dry_days = fields[3]


class Groundwater(Section):
    """Link a subcatchment to an aquifer and to a drainage system node"""

    field_format = "{:16}\t{:16}\t{:16}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}\t{:6}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)  # set_text will call __init__ without new_text to do the initialization below
        else:
            Section.__init__(self)
            self.subcatchment = ''
            """Subcatchment name"""

            self.aquifer = ''
            """Aquifer that supplies groundwater. None = no groundwater flow."""

            self.receiving_node = ''
            """Node that receives groundwater from the aquifer."""

            self.surface_elevation = ''
            """Elevation of ground surface for the subcatchment
                that lies above the aquifer (feet or meters)."""

            self.groundwater_flow_coefficient = ''
            """Value of A1 in the groundwater flow formula."""

            self.groundwater_flow_exponent = ''
            """Value of B1 in the groundwater flow formula."""

            self.surface_water_flow_coefficient = ''
            """Value of A2 in the groundwater flow formula."""

            self.surface_water_flow_exponent = ''
            """Value of B2 in the groundwater flow formula."""

            self.surface_gw_interaction_coefficient = ''
            """Value of A3 in the groundwater flow formula."""

            self.fixed_surface_water_depth = ''
            """Fixed depth of surface water at the receiving node (feet or meters)
                (set to zero if surface water depth will vary
                 as computed by flow routing).
                This value is used to compute HSW."""

            self.threshold_groundwater_elevation = ''
            """Groundwater elevation that must be reached before any flow occurs
                (feet or meters).
                Leave blank to use the receiving node's invert elevation."""

            self.bottom_elevation = ''
            """override bottom elevation aquifer parameter"""

            self.water_table_elevation = ''
            """override initial water table elevation aquifer parameter"""

            self.unsaturated_zone_moisture = ''
            """override initial upper moisture content aquifer parameter"""

    def get_text(self):
        inp = ''
        if self.comment:
            inp = self.comment + '\n'
        inp += self.field_format.format(self.subcatchment,
                                        self.aquifer,
                                        self.receiving_node,
                                        self.surface_elevation,
                                        self.groundwater_flow_coefficient,
                                        self.groundwater_flow_exponent,
                                        self.surface_water_flow_coefficient,
                                        self.surface_water_flow_exponent,
                                        self.surface_gw_interaction_coefficient,
                                        self.fixed_surface_water_depth,
                                        self.threshold_groundwater_elevation,
                                        self.bottom_elevation,
                                        self.water_table_elevation,
                                        self.unsaturated_zone_moisture)
        return inp

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 0:
            self.subcatchment = fields[0]
        if len(fields) > 1:
            self.aquifer = fields[1]
        if len(fields) > 2:
            self.receiving_node = fields[2]
        if len(fields) > 3:
            self.surface_elevation = fields[3]
        if len(fields) > 4:
            self.groundwater_flow_coefficient = fields[4]
        if len(fields) > 5:
            self.groundwater_flow_exponent = fields[5]
        if len(fields) > 6:
            self.surface_water_flow_coefficient = fields[6]
        if len(fields) > 7:
            self.surface_water_flow_exponent = fields[7]
        if len(fields) > 8:
            self.surface_gw_interaction_coefficient = fields[8]
        if len(fields) > 9:
            self.fixed_surface_water_depth = fields[9]
        if len(fields) > 10:
            self.threshold_groundwater_elevation = fields[10]
        if len(fields) > 11:
            self.bottom_elevation = fields[11]
        if len(fields) > 12:
            self.water_table_elevation = fields[12]
        if len(fields) > 13:
            self.unsaturated_zone_moisture = fields[13]


class LIDUsage(Section):
    """Specifies how an LID control will be deployed in a subcatchment"""

    field_format = " {:15}\t{:16}\t{:7}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}\t{:24}"  # TODO: add fields? \t{:24}\t{:16}

    def __init__(self, new_text=None):

        if new_text:
            self.set_text(new_text)
        else:
            Section.__init__(self)
            self.subcatchment_name = ''
            """Name of the Subcatchment defined in [SUBCATCHMENTS] where this usage occurs"""

            self.control_name = ''
            """Name of the LID control defined in [LID_CONTROLS] to be used in the subcatchment"""

            self.number_replicate_units = '0'
            """Number of equal size units of the LID practice deployed within the subcatchment"""

            self.area_each_unit = ''
            """Surface area devoted to each replicate LID unit"""

            self.top_width_overland_flow_surface = ''
            """Width of the outflow face of each identical LID unit"""

            self.percent_initially_saturated = ''
            """Degree to which storage zone is initially filled with water"""

            self.percent_impervious_area_treated = ''
            """Percent of the impervious portion of the subcatchment's non-LID area whose runoff
            is treated by the LID practice"""

            self.send_outflow_pervious_area = '0'
            """1 if the outflow from the LID is returned onto the subcatchment's pervious area rather
            than going to the subcatchment's outlet"""

            self.detailed_report_file = ""
            """Name of an optional file where detailed time series results for the LID will be written"""

    def get_text(self):
        inp = ''
        if self.comment:
            inp = self.comment + '\n'
        inp += LIDUsage.field_format.format(self.subcatchment_name,
                                            self.control_name,
                                            self.number_replicate_units,
                                            self.area_each_unit,
                                            self.top_width_overland_flow_surface,
                                            self.percent_initially_saturated,
                                            self.percent_impervious_area_treated,
                                            self.send_outflow_pervious_area,
                                            self.detailed_report_file)
        return inp

    def set_text(self, new_text):
        self.__init__()
        fields = new_text.split()
        if len(fields) > 0:
            self.subcatchment_name = fields[0]
        if len(fields) > 1:
            self.control_name = fields[1]
        if len(fields) > 2:
            self.number_replicate_units = fields[2]
        if len(fields) > 3:
            self.area_each_unit = fields[3]
        if len(fields) > 4:
            self.top_width_overland_flow_surface = fields[4]
        if len(fields) > 5:
            self.percent_initially_saturated = fields[5]
        if len(fields) > 6:
            self.percent_impervious_area_treated = fields[6]
        if len(fields) > 7:
            self.send_outflow_pervious_area = fields[7]
        if len(fields) > 8:
            self.detailed_report_file = fields[8]


class Coverage(Section):
    """Specifies the percentage of a subcatchments area that is covered by each category of land use."""

    field_format = "{:16}\t{:16}\t{:10}"

    def __init__(self, subcatchment_name = '', land_use_name = '', percent_subcatchment_area = ''):
        Section.__init__(self)

        self.subcatchment_name = subcatchment_name
        """Name of the Subcatchment defined in [SUBCATCHMENTS] where this coverage occurs"""

        self.land_use_name = land_use_name
        """land use name from [LANDUSE] of this coverage"""

        self.percent_subcatchment_area = percent_subcatchment_area
        """percent of subcatchment area covered by this land use"""

    def get_text(self):
        return self.field_format.format(self.subcatchment_name, self.land_use_name, self.percent_subcatchment_area)


class Coverages(Section):
    """Specifies the percentage of a subcatchments area that is covered by each category of land use."""

    SECTION_NAME = "[COVERAGES]"
    DEFAULT_COMMENT = ";;Subcatchment  \tLand Use        \tPercent\n"\
                      ";;--------------\t----------------\t----------"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            Section.__init__(self)
            self.value = []

    def get_text(self):
        lines = []
        if len(self.value) > 0:
            lines.append(self.SECTION_NAME)
            if self.comment:
                if self.comment.startswith(';'):
                    lines.append(self.comment)
                else:
                    lines.append(';' + self.comment.replace('\n', '\n;'))
            num_this_line = 0
            for coverage in self.value:
                lines.append(coverage.get_text())
        return '\n'.join(lines)

    def set_text(self, new_text):
        self.__init__()
        for line in new_text.splitlines():
            line = self.set_comment_check_section(line)
            fields = line.split()
            if len(fields) > 2:
                subcatchment = fields[0]
                for landuse_index in range(1, len(fields) - 1, 2):
                    self.value.append(Coverage(subcatchment, fields[landuse_index], fields[landuse_index+1]))


class InitialLoading(Section):
    """Specifies the pollutant buildup that exists on each subcatchment at the start of a simulation."""

    field_format = "{:16}\t{:16}\t{:10}"

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            Section.__init__(self)
            self.subcatchment_name = ''
            """Name of the Subcatchment defined in [SUBCATCHMENTS] where this loading occurs"""

            self.pollutant_name = ""
            """name of a pollutant"""

            self.initial_buildup = 0
            """initial buildup of pollutant (lbs/acre or kg/hectare)"""

    def get_text(self):
        inp = ''
        if self.comment:
            inp = self.comment + '\n'
        inp += self.field_format.format(self.subcatchment_name,
                                        self.pollutant_name,
                                        self.initial_buildup)
        return inp

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split()
        if len(fields) > 2:
            self.subcatchment_name = fields[0]
            self.pollutant_name = fields[1]
            self.initial_buildup = fields[2]
