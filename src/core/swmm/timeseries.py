import core.coordinates


class TimeSeries:
    """class for time series data"""
    def __init__(self):
        self.name = ""
        """name of timeseries"""

        self.description = ""
        """timeseries description"""

        self.date_time = ()			# string
        """date/time string"""

        self.value = ()
        """timeseries values"""

        self.file = ""
        """file name if timeseries read from file"""

