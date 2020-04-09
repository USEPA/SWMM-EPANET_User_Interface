from core.project_base import Section


class TimeSeries(Section):
    """One time series from the TIMESERIES section"""

    def __init__(self):
        Section.__init__(self)

        ## name of timeseries
        self.name = "Unnamed"

        ## file name if timeseries read from file
        self.file = ''

        ## List of Dates
        self.dates = []

        ## List of Times
        self.times = []

        ## List of Values
        self.values = []


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

