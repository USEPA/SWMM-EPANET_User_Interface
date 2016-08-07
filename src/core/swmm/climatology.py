from enum import Enum
from core.project_base import Section
from core.swmm.timeseries import TimeSeries


class TemperatureSource(Enum):
    UNSET = 0
    TIMESERIES = 1
    FILE = 2


class EvaporationFormat(Enum):
    UNSET = 0
    CONSTANT = 1     # (in/day or mm/day)
    MONTHLY = 2      # evaporation for each month: Jan Feb ... Dec (in/day or mm/day)
    TIMESERIES = 3   # name of timeseries with evaporation data
    TEMPERATURE = 4  # compute from daily air temperature and latitude
    FILE = 5         # pan for each month: Jan Feb ... Dec


class WindSource(Enum):
    MONTHLY = 0
    FILE = 1


class Temperature(Section):
    """temperature, wind speed, snow melt, and areal depletion parameters"""

    SECTION_NAME = "[TEMPERATURE]"


    def __init__(self):
        Section.__init__(self)

        self.source = TemperatureSource.UNSET
        """source of temperature data; timeseries or file"""

        self.timeseries = ''
        """name of time series in [TIMESERIES] section"""

        self.filename = ''
        """name of external Climate file with temperature data."""

        self.start_date = ''
        """date to begin reading from the file m/d/y. If unset, read all"""

        self.wind_speed = WindSpeed()

        self.snow_melt = SnowMelt()

        self.areal_depletion = ArealDepletion()


class Evaporation(Section):
    """How daily evaporation rates vary with time for the study area"""

    SECTION_NAME = "[EVAPORATION]"

    def __init__(self):
        Section.__init__(self)

        self.format = EvaporationFormat.UNSET
        """format used for evaporation data"""

        self.constant = ''
        """a constant evaporation rate"""

        self.monthly = ()
        """twelve monthly evaporation rates"""

        self.timeseries = ''
        """name of time series in [TIMESERIES] section with evaporation data"""

        self.monthly_pan_coefficients = ()
        """twelve monthly pan coefficients used with file option and file name in temperature section"""

        self.recovery_pattern = ''  # time pattern ID
        """name of a monthly time pattern"""

        self.dry_only = False
        """determines if evaporation only occurs during periods with no precipitation."""

        self.dry_only_specified = False
        """ True if DRY_ONLY was included when read from text.
            If dry_only_specified == False, then DRY_ONLY is skipped in get_text if self.dry_only_specified == False.
            If dry_only_specified == True, DRY_ONLY will be included in get_text even if self.dry_only == False. """


class WindSpeed:
    """wind speed parameters, stored as part of [TEMPERATURE] section"""

    SECTION_NAME = "WINDSPEED"

    def __init__(self):
        self.source = WindSource.MONTHLY
        """Whether wind speed is entered from the climate file or as monthly values"""

        self.wind_speed_monthly = ()
        """Average wind speed each month (Jan, Feb ... Dec) (mph or km/hr)"""


class SnowMelt:
    """snow melt parameters"""

    SECTION_NAME = "SNOWMELT"

    def __init__(self):
        self.snow_temp = ''
        """air temperature at which precipitation falls as snow (deg F or C)"""

        self.ati_weight = '0.5'
        """antecedent temperature index weight (default is 0.5)"""

        self.negative_melt_ratio = '0.6'
        """negative melt ratio (default is 0.6)"""

        self.elevation = '0'
        """average elevation of study area above mean sea level (ft or m)"""

        self.latitude = '0.0'
        """latitude of the study area in degrees North (default is 50)."""

        self.time_correction = '0'
        """correction, in minutes of time, between true solar time and the standard clock time (default is 0)."""


class ArealDepletion:
    """areal depletion parameters"""

    SECTION_NAME = "ADC"

    def __init__(self):
        self.adc_impervious = ()
        """fraction of area covered by snow when ratio of snow depth to depth for impervious area"""

        self.adc_pervious = ()
        """fraction of area covered by snow when ratio of snow depth to depth for pervious area"""


class Adjustments(Section):
    """Specifies optional monthly adjustments to be made to temperature, evaporation rate,
    rainfall intensity and hydraulic conductivity in each time period of a simulation."""

    SECTION_NAME = "[ADJUSTMENTS]"

    def __init__(self):
        Section.__init__(self)
        self.temperature = []
        """monthly temperature adjustments as plus or minus degrees F (degrees C)"""

        self.evaporation = []
        """monthly evaporation adjustments as plus or minus in/day (mm/day)"""

        self.rainfall = []
        """monthly rain adjustments as multipliers applied to precipitation rate"""

        self.soil_conductivity = []
        """monthly soil_conductivity adjustments as multipliers applied to soil hydraulic conductivity"""
