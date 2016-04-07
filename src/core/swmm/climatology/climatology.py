from enum import Enum
from core.inputfile import Section
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

    first_field_format = "{:18}"

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

    def get_text(self):
        # If not set, need to leave entire section out of inp file
        if self.source == TemperatureSource.UNSET:
            return ''

        text_list = [self.SECTION_NAME]

        if self.comment:
            text_list.append(self.comment)

        field_start = Temperature.first_field_format.format(self.source.name) + '\t'
        if self.source == TemperatureSource.TIMESERIES and self.timeseries:
            text_list.append(field_start + self.timeseries)
        elif self.source == TemperatureSource.FILE and self.filename:
            text_list.append(field_start + self.filename + '\t' + self.start_date)

        text_list.append(self.wind_speed.get_text())
        text_list.append(self.snow_melt.get_text())
        text_list.append(self.areal_depletion.get_text())
        return '\n'.join(text_list)

    def set_text(self, new_text):
        self.__init__()
        areal_depletion_text = ''
        for line in new_text.splitlines():
            try:
                line = self.set_comment_check_section(line)
                fields = line.split()
                if len(fields) > 1:
                    if fields[0].upper() == "TIMESERIES":
                        self.timeseries = ' '.join(fields[1:])
                        self.source = TemperatureSource.TIMESERIES
                    elif fields[0].upper() == "FILE":
                        # Check for optional start date as last field
                        if TimeSeries.is_date(fields[-1]):
                            self.start_date = fields[-1]
                            self.filename = ' '.join(fields[1:-1])
                        else:
                            self.filename = ' '.join(fields[1:])
                        self.source = TemperatureSource.FILE
                    elif fields[0].upper() == WindSpeed.SECTION_NAME:
                        self.wind_speed = WindSpeed()
                        self.wind_speed.set_text(line)
                    elif fields[0].upper() == SnowMelt.SECTION_NAME:
                        self.snow_melt = SnowMelt()
                        self.snow_melt.set_text(line)
                    elif fields[0].upper() == ArealDepletion.SECTION_NAME:
                        if areal_depletion_text:
                            areal_depletion_text += '\n'
                        areal_depletion_text += line
            except:
                print(self.SECTION_NAME + " skipping input line: " + line)
        if areal_depletion_text:
            self.areal_depletion = ArealDepletion()
            self.areal_depletion.set_text(areal_depletion_text)


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

    def get_text(self):
        text_list = [self.SECTION_NAME]

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
        text_list.append(format_line)

        if self.recovery_pattern:
            text_list.append("RECOVERY\t" + self.recovery_pattern)

        if self.dry_only:
            text_list.append("DRY_ONLY\tYES")
        else:
            text_list.append("DRY_ONLY\tNO")
        return '\n'.join(text_list)

    def set_text(self, new_text):
        self.__init__()
        for line in new_text.splitlines():
            line = self.set_comment_check_section(line)
            fields = line.split()
            if len(fields) > 1:
                if fields[0].upper() == "DRY_ONLY":
                    self.dry_only = fields[1].upper() == "YES"
                elif fields[0].upper() == "RECOVERY":
                    self.recovery_pattern = ' '.join(fields[1:])
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
                    except Exception as ex:
                        raise ValueError("Could not set " + self.SECTION_NAME + " from: " + line + '\n' + str(ex))


class WindSpeed:
    """wind speed parameters, stored as part of [TEMPERATURE] section"""

    SECTION_NAME = "WINDSPEED"

    def __init__(self):
        self.source = WindSource.MONTHLY
        """Whether wind speed is entered from the climate file or as monthly values"""

        self.wind_speed_monthly = ()
        """Average wind speed each month (Jan, Feb ... Dec) (mph or km/hr)"""

    def get_text(self):
        inp = Temperature.first_field_format.format(WindSpeed.SECTION_NAME) + '\t' + self.source.name
        if self.source == WindSource.MONTHLY:
            if len(self.wind_speed_monthly) > 0:
                inp += '\t' + '\t'.join(self.wind_speed_monthly)
            else:
                inp = ''
        elif self.source == WindSource.FILE:
            pass
        else:
            inp = ''
        return inp

    def set_text(self, new_text):
        self.__init__()
        fields = new_text.split()
        if len(fields) > 1:
            if fields[0].strip().upper() != self.SECTION_NAME:
                raise ValueError("Could not set " + self.SECTION_NAME + " from: " + new_text)
            self.source = WindSource[fields[1].upper()]
        if len(fields) > 2 and self.source == WindSource.MONTHLY:
            self.wind_speed_monthly = fields[2:]


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

    def get_text(self):
        return Temperature.first_field_format.format(SnowMelt.SECTION_NAME) + '\t' +\
               self.snow_temp + '\t' +\
               self.ati_weight + '\t' +\
               self.negative_melt_ratio + '\t' +\
               self.elevation + '\t' +\
               self.latitude + '\t' +\
               self.time_correction

    def set_text(self, new_text):
        self.__init__()
        fields = new_text.split()
        if len(fields) > 0:
            if fields[0].strip().upper() != self.SECTION_NAME:
                raise ValueError("Could not set " + self.SECTION_NAME + " from: " + new_text)
        if len(fields) > 1:
           self.snow_temp = fields[1]
        if len(fields) > 2:
           self.ati_weight = fields[2]
        if len(fields) > 3:
           self.negative_melt_ratio = fields[3]
        if len(fields) > 4:
           self.elevation = fields[4]
        if len(fields) > 5:
           self.latitude = fields[5]
        if len(fields) > 6:
           self.time_correction = fields[6]


class ArealDepletion:
    """areal depletion parameters"""

    SECTION_NAME = "ADC"

    def __init__(self):
        self.adc_impervious = ()
        """fraction of area covered by snow when ratio of snow depth to depth for impervious area"""

        self.adc_pervious = ()
        """fraction of area covered by snow when ratio of snow depth to depth for pervious area"""

    def get_text(self):
        text_list = []
        if len(self.adc_impervious) > 0:
            text_list.append("ADC IMPERVIOUS\t" + '\t'.join(self.adc_impervious))
        if len(self.adc_impervious) > 0:
            text_list.append("ADC PERVIOUS\t" + '\t'.join(self.adc_pervious))
        return '\n'.join(text_list)

    def set_text(self, new_text):
        self.__init__()
        for line in new_text.splitlines():
            fields = line.split()
            if len(fields) > 2:
                if fields[0].strip().upper() != self.SECTION_NAME:
                    raise ValueError("Could not set " + self.SECTION_NAME + " from: " + line)
                if fields[1].upper() == "IMPERVIOUS":
                    self.adc_impervious = fields[2:]
                elif fields[1].upper() == "PERVIOUS":
                    self.adc_pervious = fields[2:]


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

    def get_text(self):
        text_list = []
        for (data, default, label) in ((self.temperature,       "0.0", "TEMPERATURE"),
                                       (self.evaporation,       "0.0", "EVAPORATION"),
                                       (self.rainfall,          "1.0", "RAINFALL"),
                                       (self.soil_conductivity, "1.0", "CONDUCTIVITY")):
            values = self.format_values(data, default)
            if values:
                text_list.append(label + '\t' + values)

        # Only add section name and comment if there is some content in this section
        if len(text_list) > 0:
            text_list.insert(0, self.SECTION_NAME)
            if self.comment:
                text_list.insert(1, self.comment)
        return '\n'.join(text_list)

    @staticmethod
    def format_values(data, default):
        """Format list of data values into a string. Blank values are replaced by default.
         If all are blank or default, return empty string, otherwise return tab-separated values."""
        formatted = ''
        any_value = False
        if data and len(data) > 11:
            for value in data:
                value = str(value).strip()
                if len(value) == 0:
                    value = default
                elif value != default and value != default.rstrip(".0"):
                    any_value = True
                if formatted:
                    formatted += '\t'
                formatted += value
        if any_value:
            return formatted
        else:
            return ''

    def set_text(self, new_text):
        self.__init__()
        for line in new_text.splitlines():
            try:
                line = self.set_comment_check_section(line)
                fields = line.split()
                if len(fields) > 12:
                    if fields[0].upper() == "TEMPERATURE":
                        self.temperature = fields[1:]
                    elif fields[0].upper() == "EVAPORATION":
                        self.evaporation = fields[1:]
                    elif fields[0].upper() == "RAINFALL":
                        self.rainfall = fields[1:]
                    elif fields[0].upper() == "CONDUCTIVITY":
                        self.soil_conductivity = fields[1:]
            except:
                print(self.SECTION_NAME + " skipping input line: " + line)
