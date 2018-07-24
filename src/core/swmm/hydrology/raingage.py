from core.coordinate import Coordinate
import core.swmm.timeseries
from enum import Enum
from core.metadata import Metadata
from core.project_base import Section


class RainFormat(Enum):
    """Format in which the rain data are supplied:
        INTENSITY: each rainfall value is an average rate in inches/hour
        (or mm/hour) over the recording interval,
        VOLUME: each rainfall value is the volume of rain that fell in the
        recording interval (in inches or millimeters),
        CUMULATIVE: each rainfall value represents the cumulative
        rainfall that has occurred since the start of."""
    INTENSITY = 1
    VOLUME = 2
    CUMULATIVE = 3


class RainDataSource(Enum):
    TIMESERIES = 1
    FILE = 2


class RainFileUnits(Enum):
    IN = 1
    MM = 2


class RainGage(Section, Coordinate):
    """A rain gage, including reference to location and time-series data"""

    #    attribute,         input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",                    '', "Name",                  "",       '', '', "User-assigned name of rain gage"),
        ("x",                       '', "X-Coordinate",          "",       '', '', "X coordinate of rain gage on study area map"),
        ("y",                       '', "Y-Coordinate",          "",       '', '', "Y coordinate of rain gage on study area map"),
        ("description",             '', "Description",           "",       '', '', "Optional comment or description"),
        ("tag",                     '', "Tag",                   "",       '', '', "Optional category or classification"),
        ("rain_format",             '', "Rain Format",           "",       '', '', "Type of rainfall data recorded at rain gage"),
        ("rain_interval",           '', "Time Interval",         "1:00",   '', '', "Data recording time intervals at rain gage"),
        ("snow_catch_factor",       '', "Snow Catch Factor",     "1",      '', '', "Correction factor applied to snowfall"),
        ("data_source",             '', "Data Source",           "",       '', '', "Source of rainfall data"),
        ("timeseries",              '', "Time Series Name",      "",       '', '', "Name of rainfall time series"),
        ("data_file_name",          '', "Data File Name",        "",       '', '', "Name of rainfall data file"),
        ("data_file_station_id",    '', "Data File Station ID",  "",       '', '', "Station ID contained in data file"),
        ("data_file_rain_units",    '', "Data file Rain Units",  "",       '', '', "Units of rainfall data")
    ))

    def __init__(self):
        Section.__init__(self)
        Coordinate.__init__(self)

        ## Optional description of the gage
        self.description = ''

        ## Optional label used to categorize the gage
        self.tag = ''

        ## Format in which the rain data are supplied:
        ## INTENSITY, VOLUME, CUMULATIVE (see also self.rain_units)
        self.rain_format = RainFormat.VOLUME

        ## Recording time interval between gage readings in either decimal
        ## hours or hours:minutes format.
        self.rain_interval = "1:00"

        ## Factor that corrects gage readings for snowfall
        self.snow_catch_factor = 1.0

        ## Source of rainfall data; This can be set to a
        ## TimeSeries or a TimeSeriesFile.
        self.data_source = RainDataSource.TIMESERIES

        ## name of time series with rainfall data if Data Source selection was TIMESERIES
        self.timeseries = "None"

        ## Name of external file containing rainfall data
        self.data_file_name = "None"

        ## Recording gage station number
        self.data_file_station_id = "StationID"

        ## Depth units (IN or MM) for rainfall values in the file
        self.data_file_rain_units = RainFileUnits.IN
