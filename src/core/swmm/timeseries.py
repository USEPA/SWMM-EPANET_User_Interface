from core.project_base import Section


class TimeSeries(Section):
    """One time series from the TIMESERIES section"""

    def __init__(self):
        Section.__init__(self)

        self.name = "Unnamed"
        """name of timeseries"""

        self.file = ''
        """file name if timeseries read from file"""

        self.dates = []
        """List of Dates"""

        self.times = []
        """List of Times"""

        self.values = []
        """List of Values"""

    @staticmethod
    def is_date(test_string):
        if len(test_string) > 5:
            check_split = test_string.strip().split('/')
            if len(check_split) != 3:
                check_split = test_string.strip().split('-')
            if len(check_split) == 3 and ''.join(check_split).isdigit() and \
               0 < int(check_split[0]) <= 12 and \
               0 < int(check_split[1]) <= 31 and \
               0 < int(check_split[2]) <= 3000:
                return True
        return False

