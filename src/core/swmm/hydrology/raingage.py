from core.coordinates import Coordinates
from enum import Enum


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


class RainGage:
    """A rain gage, including reference to location and time-series data"""

    def __init__(self, name):
        self.name = name
        """User-assigned rain gage name"""

        self.coordinates = Coordinates(None, None)
        """Location of gage; If not set, gage will not appear on the map."""

        self.description = None
        """Optional description of the gage"""

        self.tag = None
        """Optional label used to categorize the gage"""

        self.rain_format = RainFormat.VOLUME
        """Format in which the rain data are supplied:
            INTENSITY, VOLUME, CUMULATIVE (see also self.rain_units)"""

        self.rain_interval = 0.0
        """Recording time interval between gage readings in either decimal
            hours or hours:minutes format."""

        self.snow_catch_factor = 1
        """Factor that corrects gage readings for snowfall"""

        self.data_source = None
        """Source of rainfall data; This can be set to a
            TimeSeries or a TimeSeriesFile."""
