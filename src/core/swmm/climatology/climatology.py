from enum import Enum
from core.inputfile import Section


class TemperatureSource(Enum):
    TIMESERIES = 0
    FILE = 1


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


class Evaporation(Section):
    """How daily evaporation rates vary with time for the study area"""

    SECTION_NAME = "[EVAPORATION]"

    def __init__(self):
        Section.__init__(self)

        self.format = EvaporationFormat.UNSET
        """format used for evaporation data"""

        self.constant = 0.0
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

    def get_text(self):
        text_list = [self.name]

        if self.comment:
            text_list.append(self.comment)

        format_line = self.format.name + '\t'
        if self.format == EvaporationFormat.CONSTANT:
            format_line += self.constant
        elif self.format == EvaporationFormat.MONTHLY:
            format_line += '\t'.join(self.monthly)
        elif self.format == EvaporationFormat.TIMESERIES:
            format_line += self.timeseries
        elif self.format == EvaporationFormat.TEMPERATURE:
            pass
        elif self.format == EvaporationFormat.FILE:
            format_line += '\t'.join(self.monthly_pan_coefficients)
        elif self.format == EvaporationFormat.RECOVERY:
            format_line += self.recovery_pattern
        text_list.append(format_line)

        if self.dry_only:
            text_list.append("DRY_ONLY\tYES")
        else:
            text_list.append("DRY_ONLY\tNO")
        return '\n'.join(text_list)

    def set_text(self, new_text):
        self.__init__()
        for line in new_text.splitlines():
            if line.startswith('['):
                if line.strip().upper() != self.name.upper():
                    raise ValueError("Cannot set " + self.name + " from section " + line.strip())
            elif line.startswith(';'):
                if self.comment:
                    self.comment += '\n'
                self.comment += line
            else:
                fields = line.split()
                if len(fields) > 0:
                    if fields[0].upper() == "DRY_ONLY":
                        self.dry_only = fields[1].upper() == "YES"
                    else:
                        try:
                            self.format = EvaporationFormat[fields[0]]
                            if self.format == EvaporationFormat.CONSTANT:
                                self.constant = fields[1]
                            elif self.format == EvaporationFormat.MONTHLY:
                                self.monthly = fields[1:]
                            elif self.format == EvaporationFormat.TIMESERIES:
                                self.timeseries = fields[1]
                            elif self.format == EvaporationFormat.TEMPERATURE:
                                pass
                            elif self.format == EvaporationFormat.FILE:
                                self.monthly_pan_coefficients = fields[1:]
                            elif self.format == EvaporationFormat.RECOVERY:
                                self.recovery_pattern = fields[1]
                        except Exception as ex:
                            raise ValueError("Could not set EVAPORATION from: " + line + '\n' + str(ex))

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
