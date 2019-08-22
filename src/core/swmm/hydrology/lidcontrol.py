from enum import Enum
from core.project_base import Section


class LIDType(Enum):
    # BC for bio-retention cell; RG for rain garden; GR for green roof; PP for porous pavement;
        # IT for infiltration trench; RB for rain barrel;RD for rooftup disconnect; VS for vegetative swale.
    BC = 1
    RG = 2
    GR = 3
    IT = 4
    PP = 5
    RB = 6
    RD = 7
    VS = 8


class LIDControl(Section):
    """Defines scale-independent LID controls that can be deployed within subcatchments"""

    LineTypes = (
        ("has_surface_layer",
         "SURFACE",
         "surface_layer_storage_depth",
         "surface_layer_vegetative_cover_fraction",
         "surface_layer_surface_roughness",
         "surface_layer_surface_slope",
         "surface_layer_swale_side_slope"),
        ("has_soil_layer",
         "SOIL",
         "soil_layer_thickness",
         "soil_layer_porosity",
         "soil_layer_field_capacity",
         "soil_layer_wilting_point",
         "soil_layer_conductivity",
         "soil_layer_conductivity_slope",
         "soil_layer_suction_head"),
        ("has_pavement_layer",
         "PAVEMENT",
         "pavement_layer_thickness",
         "pavement_layer_void_ratio",
         "pavement_layer_impervious_surface_fraction",
         "pavement_layer_permeability",
         "pavement_layer_clogging_factor",
         "pavement_layer_regeneration_interval",
         "pavement_layer_regeneration_fraction"),
        ("has_storage_layer",
         "STORAGE",
         "storage_layer_height",
         "storage_layer_void_ratio",
         "storage_layer_filtration_rate",
         "storage_layer_clogging_factor"),
        ("has_underdrain_system",
         "DRAIN",
         "drain_coefficient",
         "drain_exponent",
         "drain_offset_height",
         "drain_delay",
         "drain_open_level",
         "drain_closed_level",
         "drain_control_curve"),
        ("has_drainmat_system",
         "DRAINMAT",
         "drainmat_thickness",
         "drainmat_void_fraction",
         "drainmat_roughness"),
        ("has_pollutant_removals",
         "REMOVALS",
         "removal_pollutant1",
         "removal_removal1",
         "removal_pollutant2",
         "removal_removal2",
         "removal_pollutant3",
         "removal_removal3",
         "removal_pollutant4",
         "removal_removal4",
         "removal_pollutant5",
         "removal_removal5"))

    def __init__(self):
        Section.__init__(self)

        ## Name used to identify the particular LID control
        self.name = "Unnamed"

        ## Generic type of LID being defined
        self.lid_type = LIDType.BC

        ## does lid have surface layer
        self.has_surface_layer = False

        ## does lid have pavement layer
        self.has_pavement_layer = False

        ## does lid have soil layer
        self.has_soil_layer = False

        ## does lid have storage layer
        self.has_storage_layer = False

        ## does lid have underdrain system
        self.has_underdrain_system = False

        ## does lid have drainmat system
        self.has_drainmat_system = False

        ## does lid have pollutant removals
        self.has_pollutant_removals = False

        ## When confining walls or berms are present this is the maximum depth to
        ## which water can pond above the surface of the unit before overflow
        ## occurs (in inches or mm). For LIDs that experience overland flow it is
        ## the height of any surface depression storage. For swales, it is the height
        ## of its trapezoidal cross section.
        self.surface_layer_storage_depth = "0.0"

        ## Fraction of the storage area above the surface that is filled with vegetation
        self.surface_layer_vegetative_cover_fraction = "0.0"

        ## Manning's n for overland flow over the surface of porous pavement or a vegetative swale
        self.surface_layer_surface_roughness = "0.1"

        ## Slope of porous pavement surface or vegetative swale
        self.surface_layer_surface_slope = "1.0"

        ## Slope (run over rise) of the side walls of a vegetative swale's cross section
        self.surface_layer_swale_side_slope = "5.0"

        ## Thickness of the pavement layer
        self.pavement_layer_thickness = "0.0"

        ## Volume of void space relative to the volume of solids in the pavement
        self.pavement_layer_void_ratio = "0.15"

        ## Ratio of impervious paver material to total area for modular systems
        self.pavement_layer_impervious_surface_fraction = "0.0"

        ## Permeability of the concrete or asphalt used in continuous systems or hydraulic
        ## conductivity of the fill material (gravel or sand) used in modular systems
        self.pavement_layer_permeability = "100.0"

        ## Number of pavement layer void volumes of runoff treated it takes to completely clog the pavement
        self.pavement_layer_clogging_factor = "0.0"

        ## The number of days that the pavement layer is allowed to clog before its permeability is restored,
        ##  typically by vacuuming its surface. A value of 0 (the default) indicates that no permeability regeneration occurs.
        self.pavement_layer_regeneration_interval = '0'

        ## The fractional degree to which the pavement's permeability is restored when a regeneration interval is reached.
        ##  The default is 0 (no restoration) while a value of 1 indicates complete restoration to the original permeability value.
        self.pavement_layer_regeneration_fraction = '0'

        ## Thickness of the soil layer
        self.soil_layer_thickness = "0.0"

        ## Volume of pore space relative to total volume of soil
        self.soil_layer_porosity = "0.5"

        ## Volume of pore water relative to total volume after the soil has been allowed to drain fully
        self.soil_layer_field_capacity = "0.2"

        ## Volume of pore water relative to total volume for a well dried soil where only bound water remains
        self.soil_layer_wilting_point = "0.1"

        ## Hydraulic conductivity for the fully saturated soil
        self.soil_layer_conductivity = "0.5"

        ## Slope of the curve of log(conductivity) versus soil moisture content
        self.soil_layer_conductivity_slope = "10.0"

        ## Average value of soil capillary suction along the wetting front
        self.soil_layer_suction_head = "3.5"

        ## Height of a rain barrel or thickness of a gravel layer
        self.storage_layer_height = "0.0"

        ## Volume of void space relative to the volume of solids in the layer
        self.storage_layer_void_ratio = "0.75"

        ## Maximum rate at which water can flow out the bottom of the layer after it is first constructed
        self.storage_layer_filtration_rate = "0.5"

        ## Total volume of treated runoff it takes to completely clog the bottom of the layer divided by the
        ## void volume of the layer
        self.storage_layer_clogging_factor = "0.0"

        ## Coefficient that determines the rate of flow through the underdrain as a function of height of
        ## stored water above the drain height
        self.drain_coefficient = "0.0"

        ## Exponent that determines the rate of flow through the underdrain as a function of height of
        ## stored water above the drain height
        self.drain_exponent = "0.5"

        ## Height of any underdrain piping above the bottom of a storage layer or rain barrel
        self.drain_offset_height = "6.0"

        ## Number of dry weather hours that must elapse before the drain line in a rain barrel is opened
        self.drain_delay = "6.0"

        ## The height( in inches or mm) in the drain's Storage Layer that causes the drain to automatically open when
        ## the water level rises above it. The default is 0 which means that this feature is disabled.
        self.drain_open_level = '0'

        ## The height (in inches or mm) in the drain's Storage Layer that causes the drain to automatically close when
        ## the water level falls below it. The default is 0.
        self.drain_closed_level = '0'

        ## The name of an optional Control Curve that adjusts the computed drain flow as a function of the head of
        ## water above the drain. Leave blank if not applicable.
        self.drain_control_curve = ''

        ## Thickness of the drainage mat (inches or mm)
        self.drainmat_thickness = "3.0"

        ## Ratio of void volume to total volume in the mat
        self.drainmat_void_fraction = "0.5"

        ## Manning's n constant used to compute the horizontal flow rate of drained water through the mat
        self.drainmat_roughness = "0.1"

        self.removal_pollutant1 = ''
        self.removal_removal1 = '0'
        self.removal_pollutant2 = ''
        self.removal_removal2 = '0'
        self.removal_pollutant3 = ''
        self.removal_removal3 = '0'
        self.removal_pollutant4 = ''
        self.removal_removal4 = '0'
        self.removal_pollutant5 = ''
        self.removal_removal5 = '0'
