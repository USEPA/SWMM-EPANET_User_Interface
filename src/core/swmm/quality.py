from enum import Enum
from core.inputfile import Section

class BuildupFunction(Enum):
    POW = 0
    EXP = 1
    SAT = 2
    EXT = 3


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


class Landuse:
    """Identifies the various categories of land uses within the drainage area. Each subcatchment area
        can be assigned a different mix of land uses. Each land use can be subjected to a different
        street sweeping schedule."""

    def __init__(self):
        self.name = ""
        """Name assigned to the land use"""

        self.description = ""
        """Optional comment or description of the land use"""

        self.street_sweeping_interval = "30.0"
        """Days between street sweeping within the land use"""

        self.street_sweeping_availability = "0.0"
        """Fraction of the buildup of all pollutants that is available for removal by sweeping"""

        self.last_swept = "0.0"
        """Number of days since last swept at the start of the simulation"""

        self.buildups = []    # Collection of type Buildup
        """Specifies the rate at which pollutants build up over different land uses between rain events."""

        self.washoffs = []    # Collection of type Washoff
        """Specifies the rate at which pollutants are washed off from different land uses during rain events."""


class Buildup:
    """Specifies the rate at which pollutants build up over different land uses between rain events."""
    def __init__(self):
        self.pollutant = ""
        """str: Pollutant name"""

        self.function = BuildupFunction.POW
        """BuildupFunction: Type of buildup function to use for the pollutant"""

        self.max_buildup = 0.0
        """float: Maximum buildup that can occur"""

        self.rate_constant = 0.0
        """float: Time constant that governs the rate of pollutant buildup"""

        self.power_sat_constant = 0.0
        """float: Exponent C3 used in the Power buildup formula, or the half-saturation constant C2 used in the
            Saturation buildup formula"""

        self.scaling_factor = 0.0
        """float: Multiplier used to adjust the buildup rates listed in the time series"""

        self.timeseries = ""
        """str: ID of Time Series that contains buildup rates"""

        self.normalizer_name = Normalizer.AREA
        """Variable to which buildup is normalized on a per unit basis"""


class Washoff:
    """Specifies the rate at which pollutants are washed off from different land uses during rain events."""
    def __init__(self):
        self.pollutant = ""
        """Pollutant name"""

        self.function = WashoffFunction.EXP
        """Choice of washoff function to use for the pollutant"""

        self.coefficient = 0.0
        """Value of C1 in the exponential and rating curve formulas"""

        self.exponent = 0.0
        """Exponent used in the exponential and rating curve washoff formulas"""

        self.cleaning_efficiency = 0.0
        """Street cleaning removal efficiency (percent) for the pollutant"""

        self.bmp_efficiency = 0.0
        """Removal efficiency (percent) associated with any Best Management Practice that might have been implemented"""


class Pollutant(Section):
    """Identifies the pollutants being analyzed"""
    field_format = " {:16}\t{:6}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}\t{:16}\t{:10}\t{:10}\t{:10}\n"

    def __init__(self, new_text=None):
        Section.__init__(self)
        self.name = ''
        """str: Name assigned to the pollutant"""

        self.units = ConcentrationUnits.MG_per_L
        """ConcentrationUnits: Units in which the pollutant concentration is expressed"""

        self.rain_concentration = ''
        """float: Concentration of the pollutant in rain water"""

        self.gw_concentration = ''
        """float: Concentration of the pollutant in ground water"""

        self.ii_concentration = ''
        """float: Concentration of the pollutant in any Infiltration/Inflow"""

        self.dwf_concentration = ''
        """float: Concentration of the pollutant in any dry weather sanitary flow"""

        self.decay_coefficient = ''
        """float: First-order decay coefficient of the pollutant (1/days)"""

        self.snow_only = False
        """bool: buildup occurs only when there is snow cover"""

        self.co_pollutant = '*'
        """str: Name of another pollutant whose runoff concentration contributes to the
            runoff concentration of the current pollutant"""

        self.co_fraction = "0.0"
        """float: Fraction of the co-pollutant's runoff concentration that contributes to the
            runoff concentration of the current pollutant"""

        self.initial_concentration = ''

        if new_text:
            self.set_text(new_text)

    def get_text(self):
        if self.snow_only:
            snow_flag = "YES"
        else:
            snow_flag = "NO"
        return Pollutant.field_format.format(self.name,
                                             ConcentrationUnitLabels[self.units.value],
                                             self.rain_concentration,
                                             self.gw_concentration,
                                             self.ii_concentration,
                                             self.decay_coefficient,
                                             snow_flag,
                                             self.co_pollutant,
                                             self.co_fraction,
                                             self.dwf_concentration,
                                             self.initial_concentration)

    def set_text(self, new_text):
        self.__init__()
        fields = new_text.split()
        if len(fields) > 5:
            self.name = fields[0]
            self.units = ConcentrationUnits(ConcentrationUnitLabels.index(fields[1].upper()))
            self.rain_concentration = fields[2]
            self.gw_concentration = fields[3]
            self.ii_concentration = fields[4]
            self.decay_coefficient = fields[5]
        if len(fields) > 6:
            self.snow_only = fields[6].upper() == "YES"
        if len(fields) > 7:
            self.co_pollutant = fields[7]
        if len(fields) > 8:
            self.co_fraction = fields[8]
        if len(fields) > 9:
            self.dwf_concentration = fields[9]
        if len(fields) > 10:
            self.initial_concentration = fields[10]
