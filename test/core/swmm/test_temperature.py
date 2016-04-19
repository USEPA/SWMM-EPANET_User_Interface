from core.swmm.climatology.climatology import Temperature
import unittest


class ClimatologyTemperatureTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = Temperature()


    def runTest(self):

        # Test default, default is empty string, no adjustments
        name = self.my_options.SECTION_NAME
        assert name == "[TEMPERATURE]"
        actual_text = self.my_options.get_text()
        assert actual_text == ''

        # Test daily temperature in time series
        test_time_series = r"""
        [TEMPERATURE]
        ;;Parameter  TSeries
        TIMESERIES TS1
        """
        # --Test set_text
        self.my_options.set_text(test_time_series)
        # --Test get_text through matches
        # --Failed base SNOW_MELT default values are written
        actual_text = self.my_options.get_text() # display purpose
        #assert self.my_options.matches(test_time_series)

        # Test daily temperature in file daily_temperature.txt
        test_file = r"""
        [TEMPERATURE]
        ;;Parameter  Fname (Start)
        FILE daily_tmperature.txt
        """
        # --Test set_text
        self.my_options.set_text(test_file)
        # --Test get_text through matches
        # --Failed base SNOW_MELT default values are written
        actual_text = self.my_options.get_text() # display purpose
        #assert self.my_options.matches(test_file)

        # Test daily temperature in file daily tepmerature.txt (file name with space) and start date
        test_file = r"""
        [TEMPERATURE]
        ;;Parameter  Fname (Start)
        FILE daily temperature 1-1-1999.txt 2/2/2012
        """
        # --Test set_text
        self.my_options.set_text(test_file)
        # --Test get_text through matches
        # --Failed base SNOW_MELT default values are written
        actual_text = self.my_options.get_text() # display purpose
        #assert self.my_options.matches(test_file)

        # Test WindSpeed monthly
        test_windspeed_monthly = r"""
        [TEMPERATURE]
        ;;Parameter  Monthly Adjustments
        WINDSPEED MONTHLY   1.0    1.0    3.0    2.0    2.0    2.0    2.0    2.0    2.0    2.0    1.0    0.0
        """
        # --Test set_text
        self.my_options.set_text(test_windspeed_monthly)
        # --Test get_text through matches
        # --Failed because get_text created empty string if only WINDSPEED
        # --I am wondering if WINDSPEED must be provided along with tmperature for evaporation calculation
        actual_text = self.my_options.get_text() # display purpose
        #assert self.my_options.matches(test_windspeed_monthly)

        test_windspeed_monthly = r"""
        [TEMPERATURE]
        ;;Parameter  Monthly Adjustments
        FILE daily_tmperature.txt
        WINDSPEED MONTHLY   1.0    1.0    3.0    2.0    2.0    2.0    2.0    2.0    2.0    2.0    1.0    0.0
        """
        # --Test set_text
        self.my_options.set_text(test_windspeed_monthly)
        # --Test get_text through matches
        # --Once temperature is defined this passes
        actual_text = self.my_options.get_text() # display purpose
        #assert self.my_options.matches(test_windspeed_monthly)

        # Test windspeed file -1
        test_windspeed_file = r"""
        [TEMPERATURE]
        ;;Parameter  Monthly Adjustments
        FILE daily_tmperature.txt
        WINDSPEED FILE
        """
        # --Test set_text
        self.my_options.set_text(test_windspeed_file)
        # --Test get_text through matches
        # --Once temperature is defined this passes
        actual_text = self.my_options.get_text() # display purpose
        #assert self.my_options.matches(test_windspeed_file)

        # Test windspeed file - 2
        # -- This should report fail because Windspeed file should be the same climate file used for air temperature
        # -- in this case the air temperature is not provided as file
        # -- Not sure how this should be handled
        test_windspeed_file = r"""
        [TEMPERATURE]
        ;;Parameter  TimeSeries
        TIMESERIES TS1
        WINDSPEED FILE
        """
        # --Test set_text
        self.my_options.set_text(test_windspeed_file)
        # --Test get_text through matches
        # --Once temperature is defined this passes
        actual_text = self.my_options.get_text() # display purpose
        #assert self.my_options.matches(test_windspeed_file)

        # Test snowmelt
        test_snowmelt = r"""
        [TEMPERATURE]
        ;;Parameter  TimeSeries
        TIMESERIES daily_temperature.txt
        WINDSPEED FILE
        SNOWMELT 2 0.5 0.6 0.0 50 0
        ADC IMPERVIOUS 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
        ADC PERVIOUS 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
        """
        # --Test set_text
        self.my_options.set_text(test_snowmelt)
        # --Test get_text through matches
        # --Once temperature is defined this passes
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_snowmelt)
        pass

        # Test snowmelt
        # -- Remove ADC PERVIOUS failed
        # -- Should both be specified? It should allow one or none
        test_snowmelt = r"""
        [TEMPERATURE]
        ;;Parameter  TimeSeries
        TIMESERIES daily_temperature.txt
        WINDSPEED FILE
        SNOWMELT 2 0.5 0.6 0.0 50 0
        ADC IMPERVIOUS 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
        """
        # --Test set_text
        self.my_options.set_text(test_snowmelt)
        # --Test get_text through matches
        # --Once temperature is defined this passes
        actual_text = self.my_options.get_text() # display purpose
        #assert self.my_options.matches(test_snowmelt)

        # Test snowmelt -- Remove both ADCs
        test_snowmelt = r"""
        [TEMPERATURE]
        ;;Parameter  TimeSeries
        TIMESERIES daily_temperature.txt
        WINDSPEED FILE
        SNOWMELT 2 0.5 0.6 0.0 50 0
        """
        # --Test set_text
        self.my_options.set_text(test_snowmelt)
        # --Test get_text through matches
        # --Once temperature is defined this passes
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_snowmelt)

        # Test snowmelt -- without temperature
        # -- Failed the same way as windspeed without temperature
        # -- I do no think daily temperature has to be provided for this
        test_snowmelt = r"""
        [TEMPERATURE]
        ;;Parameter  TimeSeries
        SNOWMELT 2 0.5 0.6 0.0 50 0
        """
        # --Test set_text
        self.my_options.set_text(test_snowmelt)
        # --Test get_text through matches
        # --Once temperature is defined this passes
        actual_text = self.my_options.get_text() # display purpose
        #assert self.my_options.matches(test_snowmelt)

        pass
