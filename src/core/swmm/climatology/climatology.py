from enum import Enum


class TemperatureSource(Enum):
    TIMESERIES = 0
    FILE = 1


class EvaporationFormat(Enum):
    UNSET = 0
    CONSTANT = 1     # (in/day or mm/day)
    MONTHLY = 2      # evapJan evapFeb ... evapDec (in/day or mm/day)
    TIMESERIES = 3   # name of timeseries with evaporation data
    TEMPERATURE = 4  # compute from daily air temperature and latitude
    FILE = 5         # (panJan panFeb ... panDec)


class WindSource(Enum):
    MONTHLY = 0
    FILE = 1


class Temperature:
    """temperature parameters"""
    def __init__(self):
        self.source = TemperatureSource.TIMESERIES
        """source of temperature data; timeseries or file"""

        self.timeseries = None
        """name of time series in [TIMESERIES] section"""

        self.filename = None
        """name of external Climate file with temperature data."""

        self.start_date = None
        """date to begin reading from the file m/d/y. If unset, read all"""


class Evaporation:
    """How daily evaporation rates vary with time for the study area"""
    def __init__(self):
        self.format = EvaporationFormat.UNSET
        """format used for evaporation data"""

        self.constant = 0.0
        """a constant evaporation rate"""

        self.monthly = ()
        """twelve monthly evaporation rates"""

        self.timeseries = None
        """name of time series in [TIMESERIES] section with evaporation data"""

        self.monthly_pan_coefficients = {}
        """twelve monthly pan coefficients used with file option and file name in temperature section"""

        self.recovery_pattern = None  # time pattern
        """name of a monthly time pattern"""

        self.dry_only = False
        """determines if evaporation only occurs during periods with no precipitation."""


class WindSpeed:
    """wind speed parameters"""
    def __init__(self):
        self.source = WindSource.MONTHLY
        """Whether wind speed is entered from the climate file or as monthly values"""

        self.wind_speed_monthly = ()
        """Average wind speed each month (Jan, Feb ... Dec) (mph or km/hr)"""


class SnowMelt:
    """snow melt parameters"""
    def __init__(self):
        self.snow_temp = None
        """air temperature at which precipitation falls as snow (deg F or C)"""

        self.ati_weight = 0.5
        """antecedent temperature index weight (default is 0.5)"""

        self.negative_melt_ratio = 0.6
        """negative melt ratio (default is 0.6)"""

        self.elevation = 0
        """average elevation of study area above mean sea level (ft or m)"""

        self.latitude = 0.0
        """latitude of the study area in degrees North (default is 50)."""

        self.time_correction = 0.0
        """correction, in minutes of time, between true solar time and the standard clock time (default is 0)."""


class ArealDepletion:
    """areal depletion parameters"""
    def __init__(self):
        self.adc_impervious = None
        """fraction of area covered by snow when ratio of snow depth to depth for impervious area"""

        self.adc_pervious = None
        """fraction of area covered by snow when ratio of snow depth to depth for pervious area"""


class Adjustments:
    """monthly adjustments from undocumented table [ADJUSTMENTS]"""
    def __init__(self):
        self.temperature_adjustments = ()
        """monthly temperature adjustments"""

        self.evaporation_adjustments = ()
        """monthly evaporation adjustments"""

        self.rain_adjustments = ()
        """monthly rain adjustments"""

        self.soil_conductivity_adjustments = ()
        """monthly soil_conductivity adjustments"""
