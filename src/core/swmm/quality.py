from enum import Enum
from core.project_base import Section
from core.metadata import Metadata


class BuildupFunction(Enum):
    NONE = 0
    POW = 1
    EXP = 2
    SAT = 3
    EXT = 4


class Normalizer(Enum):
    AREA = 0
    CURBLENGTH = 1


class WashoffFunction(Enum):
    EXP = 0
    RC = 1
    EMC = 2


class ConcentrationUnits(Enum):
    MG_per_L = 0
    UG_per_L = 1
    Count_per_L = 2

ConcentrationUnitLabels = ["MG/L", "UG/L", "#/L"]


class Landuse(Section):
    """Identifies the various categories of land uses within the drainage area. Each subcatchment area
        can be assigned a different mix of land uses. Each land use can be subjected to a different
        street sweeping schedule."""


    #    attribute,              input_name, label,                     default, english, metric, hint
    metadata = Metadata((
        ("land_use_name",                '', "Land Use Name",                '', '', '',
         "User-assigned name of the land use."),
        ("street_sweeping_interval",     '', "Street Sweeping Interval",     '', "days", "days",
         "Time between street sweeping within the land use (0 for no sweeping)."),
        ("street_sweeping_availability", '', "Street Sweeping Availability", '', '', '',
         "Fraction of pollutant buildup that is available for removal by sweeping."),
        ("last_swept",                   '', "Last Swept",                   '', "days", "days",
         "Time since land use was last swept at the start of the simulation.")
    ))

    def __init__(self):
        Section.__init__(self)
        self.land_use_name = ""
        """Name assigned to the land use"""

        self.street_sweeping_interval = ''
        """Days between street sweeping within the land use"""

        self.street_sweeping_availability = ''
        """Fraction of the buildup of all pollutants that is available for removal by sweeping"""

        self.last_swept = ''
        """Number of days since last swept at the start of the simulation"""


class Buildup(Section):
    """Specifies the rate at which pollutants build up over different land uses between rain events."""


    """A different set of buildup property labels is used depending on the External Time Series buildup option"""

    #    attribute,    input_name, label,                 default, english, metric, hint
    metadata = Metadata((
        ("function",           '', "Function",            "NONE", '', '',
         "Buildup function: POW = power, EXP = exponential, SAT = saturation, EXT = external time series."),
        ("max_buildup",        '', "Max. Buildup",        "0.0",  '', '',
         "Maximum possible buildup (lbs (kg) per unit of normalizer variable)."),
        ("rate_constant",      '', "Rate Constant",       "0.0",  "lbs per normalizer per day",
                                                              "kg per normalizer per day",
         "Rate constant of buildup function 1/days for exponential buildup or for power buildup"),
        ("power_sat_constant", '', "Power/Sat. Constant", "0.0",  "days", "days",
         "Time exponent for power buildup or half saturation constant for saturation buildup."),
        ("normalizer",         '', "Normalizer",          "AREA", "acres", "hectares",
         "Subcatchment variable to which buildup is normalized: curb length (any units) or area.")
    ))

    #    attribute,    input_name, label,                 default, english, metric, hint
    metadata_ext = Metadata((
        ("function",           '', "Function",            "NONE", '', '',
         "Buildup function: POW = power, EXP = exponential, SAT = saturation, EXT = external time series."),
        ("max_buildup",        '', "Max. Buildup",        "0.0",  "lbs per unit of normalizer variable",
                                                                  "kg per unit of normalizer variable",
         "Maximum possible buildup."),
        ("scaling_factor",     '', "Scaling Factor",      "0.0",  '', '',
         "Scaling factor used to modify loading rates by a fixed ratio."),
        ("timeseries",         '', "Time Series",         "0.0",  "lbs per normalizer per day",
                                                                  "kg per normalizer per day",
         "Name of Time Series containing loading rates."),
        ("normalizer",         '', "Normalizer",          "AREA", "acres", "hectares",
         "Subcatchment variable to which buildup is normalized: curb length (any units) or area")
    ))

    def __init__(self):
        Section.__init__(self)
        self.land_use_name = ""
        """land use name"""

        self.pollutant = ''
        """str: Pollutant name"""

        self.function = BuildupFunction.POW
        """BuildupFunction: Type of buildup function to use for the pollutant"""

        self.rate_constant = '0.0'
        """float: Time constant that governs the rate of pollutant buildup"""

        self.power_sat_constant = '0.0'
        """float: Exponent C3 used in the Power buildup formula, or the half-saturation constant C2 used in the
            Saturation buildup formula"""

        self.max_buildup = '0.0'
        """float: Maximum buildup that can occur"""

        self.scaling_factor = '1.0'
        """float: Multiplier used to adjust the buildup rates listed in the time series"""

        self.timeseries = ''
        """str: ID of Time Series that contains buildup rates"""

        self.normalizer = Normalizer.AREA
        """Variable to which buildup is normalized on a per unit basis"""

class Washoff(Section):
    """Specifies the rate at which pollutants are washed off from different land uses during rain events."""


    #    attribute,     input_name, label,           default, english, metric, hint
    metadata = Metadata((
        ("function",            '', "Function",        "EMC", '', '',
         "Washoff function: EXP = exponential, RC = rating curve, EMC = event mean concentration."),
        ("coefficient",         '', "Coefficient",     "0.0", '', '',
         "Washoff coefficient or Event Mean Concentration (EMC)."),
        ("exponent",            '', "Exponent",        "0.0", '', '',
         "Runoff exponent in washoff function."),
        ("cleaning_efficiency", '', "Cleaning Effic.", "0.0", "percent", "percent",
         "Street cleaning removal efficiency for the pollutant."),
        ("bmp_efficiency",      '', "BMP Effic.",      "0.0", "percent", "percent",
         "Removal efficiency associated with any Best Management Practice utilized.")
    ))

    def __init__(self):
        Section.__init__(self)
        self.land_use_name = ""
        """land use name"""

        self.pollutant = ''
        """Pollutant name"""

        self.function = WashoffFunction.EXP
        """Choice of washoff function to use for the pollutant"""

        self.coefficient = '0.0'
        """Value of C1 in the exponential and rating curve formulas"""

        self.exponent = '0.0'
        """Exponent used in the exponential and rating curve washoff formulas"""

        self.cleaning_efficiency = '0.0'
        """Street cleaning removal efficiency (percent) for the pollutant"""

        self.bmp_efficiency = '0.0'
        """Removal efficiency (percent) associated with any Best Management Practice that might have been implemented"""


class Pollutant(Section):
    """Identifies the pollutants being analyzed"""

    #    attribute,       input_name, label,          default, english, metric, hint
    metadata = Metadata((
        ("name",                  '', "Name",          '',     '', '',
         "User-assigned name of the pollutant."),
        ("units",                 '', "Units",         "MG/L", '', '',
         "Concentration units for the pollutant."),
        ("rain_concentration",    '', "Rain Concen.",  "0.0",  '', '',
         "Concentration of the pollutant in rain water."),
        ("gw_concentration",      '', "GW Concen.",    "0.0",  '', '',
         "Concentration of the pollutant in ground water."),
        ("ii_concentration",      '', "I&I Concen.",   "0.0",  '', '',
         "Concentration of the pollutant in infiltration/inflow flow."),
        ("dwf_concentration",     '', "DWF Concen.",   "0.0",  '', '',
         "Concentration of the pollutant in dry weather sanitary flow."),
        ("initial_concentration", '', "Init. Concen.", "0.0",  '', '',
         "Initial concentration of the pollutant throughout the conveyance system."),
        ("decay_coefficient",     '', "Decay Coeff.",  "0.0",  "1/days", "1/days",
         "First-order decay coefficient of the pollutant."),
        ("snow_only",             '', "Snow Only",     False,  '', '',
         "Does the pollutant build up only during snowfall events?"),
        ("co_pollutant",          '', "Co-Pollutant",  '',     '', '',
         "Name of another pollutant to whose runoff concentration the current pollutant is dependent on."),
        ("co_fraction",           '', "Co-Fraction",   '',     '', '',
         "Fraction of the co-pollutant's runoff concentration that becomes the current pollutant's runoff concentration.")
    ))

    def __init__(self):
        Section.__init__(self)
        self.name = ''
        """str: Name assigned to the pollutant"""

        self.units = ConcentrationUnits.MG_per_L
        """ConcentrationUnits: Units in which the pollutant concentration is expressed"""

        self.rain_concentration = '0.0'
        """float: Concentration of the pollutant in rain water"""

        self.gw_concentration = '0.0'
        """float: Concentration of the pollutant in ground water"""

        self.ii_concentration = '0.0'
        """float: Concentration of the pollutant in any Infiltration/Inflow"""

        self.dwf_concentration = '0.0'
        """float: Concentration of the pollutant in any dry weather sanitary flow"""

        self.initial_concentration = '0.0'
        """pollutant concentration throughout the conveyance system at the start of the simulation (default is 0)"""
        
        self.decay_coefficient = '0.0'
        """float: First-order decay coefficient of the pollutant (1/days)"""

        self.snow_only = False
        """bool: buildup occurs only when there is snow cover"""

        self.co_pollutant = '*'
        """str: Name of another pollutant whose runoff concentration contributes to the
            runoff concentration of the current pollutant"""

        self.co_fraction = '0.0'
        """float: Fraction of the co-pollutant's runoff concentration that contributes to the
            runoff concentration of the current pollutant"""


