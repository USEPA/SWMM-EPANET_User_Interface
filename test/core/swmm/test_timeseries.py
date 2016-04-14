from core.swmm.timeseries import TimeSeries
import unittest


class TimeSeriesTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = TimeSeries()

    def runTest(self):

        # Test default, default is empty string
        # -- failed because SECTION_NAME missing
        name = self.my_options.SECTION_NAME
        assert name == "[TIMESERIES]"
        actual_text = self.my_options.get_text()
        assert actual_text == ''

        # Test Example in SWMM 5.1 manual Page335
        # -- Failed because of SECTION name and
        # -- Data structure
        test_manual5_1 = r"""
        [TIMESERIES]
        ;Rainfall time series with dates specified
        TS1 6-15-2001 7:00 0.1 8:00 0.2 9:00 0.05 10:00 0
        TS1 6-21-2001 4:00 0.2 5:00 0 14:00 0.1 15:00 0
        ;Inflow hydrograph - time relative to start of simulation
        HY1 0 0 1.25 100 2:30 150 3.0 120 4.5 0
        HY1 32:10 0 34.0 57 35.33 85 48.67 24 50 0
        """
        # Test set_text
        self.my_options.set_text(test_manual5_1)
        # Test get_text through matches
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_manual5_1)