import unittest
from core.swmm.climatology import Temperature


class TemperatureTest(unittest.TestCase):  # TODO: go over the tests
    """Test TEMPERATURE section"""

    def test_default(self):
        """Test default, default is empty string, no adjustments"""
        self.my_options = Temperature()
        name = self.my_options.SECTION_NAME
        assert name == "[TEMPERATURE]"
        actual_text = self.my_options.get_text()
        assert actual_text == ''

    def test_timeseries(self):
        """Test daily temperature in time series
         Must have SNOW_MELT, otherwise will fail
         because SNOW_MELT default values are written """
        test_time_series = "[TEMPERATURE]\n" \
                           " ;;Parameter  TSeries\n" \
                           " TIMESERIES TS1\n" \
                           " SNOWMELT 2 0.5 0.6 0.0 50 0\n" \
                           " ADC IMPERVIOUS 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0\n" \
                           " ADC PERVIOUS 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0"
        self.my_options = Temperature()
        self.my_options.set_text(test_time_series)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_time_series)

    def test_file(self):
        """Test daily temperature in file daily_temperature.txt"""
        # Will failed if SNOW_MELT not given
        test_file = "[TEMPERATURE]\n" \
                    " ;;Parameter  Fname (Start)\n" \
                    " FILE daily_tmperature.txt\n" \
                    " SNOWMELT 2 0.5 0.6 0.0 50 0\n" \
                    " ADC IMPERVIOUS 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0\n" \
                    " ADC PERVIOUS 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0"
        self.my_options = Temperature()
        self.my_options.set_text(test_file)
        actual_text = self.my_options.get_text() # display purpose
        self.assertTrue(self.my_options.matches(test_file),
                        'Failed because SNOW_MELT default values are written')

    def test_file_wt_date(self):
        """Test daily temperature in tepmerature.txt(file name with space) and start date"""
        # Will failed if SNOW_MELT not given
        test_file = "[TEMPERATURE]\n" \
                    " ;;Parameter  Fname (Start)\n" \
                    " FILE daily temperature 1-1-1999.txt 2/2/2012\n"\
                    " SNOWMELT 2 0.5 0.6 0.0 50 0\n" \
                    " ADC IMPERVIOUS 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0\n" \
                    " ADC PERVIOUS 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0"
        self.my_options = Temperature()
        self.my_options.set_text(test_file)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_file)

    def test_windspeed_monthly(self):
        """Test WindSpeed monthly"""
        # --Will fail if snow_melt not provided, same issue as above
        # --Will fail because get_text created empty string if only WINDSPEED
        # Note: WINDSPEED must be provided along with temperature for evaporation calculation
        test_windspeed_monthly = "[TEMPERATURE]\n" \
                                 " ;;Parameter  Monthly Adjustments\n" \
                                 " FILE daily temperature 1-1-1999.txt 2/2/2012\n" \
                                 " WINDSPEED MONTHLY   1.0    1.0    3.0    2.0    2.0" \
                                 "    2.0    2.0    2.0    2.0    2.0    1.0    0.0\n"\
                                 " SNOWMELT 2 0.5 0.6 0.0 50 0\n" \
                                 " ADC IMPERVIOUS 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0\n" \
                                 " ADC PERVIOUS 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0"
        self.my_options = Temperature()
        self.my_options.set_text(test_windspeed_monthly)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_windspeed_monthly)

    def test_windspeed_file_wt_temperature(self):
        """Test windspeed file wt temperature"""
        # --Will fail if snow_melt not provided, same issue as above
        # --Will fail if temperature not defined
        test_windspeed_file = "[TEMPERATURE]\n" \
                              ";;Parameter  Monthly Adjustments\n" \
                              "FILE daily_tmperature.txt\n" \
                              "WINDSPEED FILE\n"\
                              " SNOWMELT 2 0.5 0.6 0.0 50 0\n" \
                              " ADC IMPERVIOUS 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0\n" \
                              " ADC PERVIOUS 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0"
        self.my_options = Temperature()
        self.my_options.set_text(test_windspeed_file)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_windspeed_file)

    def test_windspeed_file_fail(self):
        """Test windspeed file - 2"""
        # -- This should report fail because Windspeed file should be the same climate file used for air temperature
        # -- in this case the air temperature is not provided as file
        # --Once temperature is defined this passes
        test_windspeed_file = r"""
        [TEMPERATURE]
        ;;Parameter  TimeSeries
        TIMESERIES TS1
        WINDSPEED FILE
        """
        self.my_options = Temperature()
        self.my_options.set_text(test_windspeed_file)
        actual_text = self.my_options.get_text() # display purpose
        self.assertFalse(self.my_options.matches(test_windspeed_file),"Should fail")

    def test_snowmelt(self):
        """Test snowmelt"""
        # --Once temperature is defined this passes
        test_snowmelt = r"""
        [TEMPERATURE]
        ;;Parameter  TimeSeries
        TIMESERIES daily_temperature.txt
        WINDSPEED FILE
        SNOWMELT 2 0.5 0.6 0.0 50 0
        ADC IMPERVIOUS 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
        ADC PERVIOUS 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
        """
        self.my_options = Temperature()
        self.my_options.set_text(test_snowmelt)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_snowmelt)

    def test_snowmelt_fail(self):
        """Test snowmelt wo one ADC PERVIOUS, assert failed
          Should both be specified. It should allow two or none"""
        test_snowmelt = r"""
        [TEMPERATURE]
        ;;Parameter  TimeSeries
        TIMESERIES daily_temperature.txt
        WINDSPEED FILE
        SNOWMELT 2 0.5 0.6 0.0 50 0
        ADC IMPERVIOUS 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
        """
        self.my_options = Temperature()
        self.my_options.set_text(test_snowmelt)
        actual_text = self.my_options.get_text() # display purpose
        self.assertFalse(self.my_options.matches(test_snowmelt))

    def test_snowmelt_wo_adc(self):
        """Test snowmelt -- Remove both ADCs"""
        test_snowmelt = r"""
        [TEMPERATURE]
        ;;Parameter  TimeSeries
        TIMESERIES daily_temperature.txt
        WINDSPEED FILE
        SNOWMELT 2 0.5 0.6 0.0 50 0
        """
        self.my_options = Temperature()
        self.my_options.set_text(test_snowmelt)
        actual_text = self.my_options.get_text() # display purpose
        self.assertTrue(self.my_options.matches(test_snowmelt))

    def test_snowmelt_wo_temperature(self):
        """Test snowmelt -- without temperature"""
        # -- I do no think daily temperature has to be provided for this
        # --Once temperature is defined this passes
        test_snowmelt = r"""
        [TEMPERATURE]
        ;;Parameter  TimeSeries
        SNOWMELT 2 0.5 0.6 0.0 50 0
        """
        self.my_options = Temperature()
        self.my_options.set_text(test_snowmelt)
        actual_text = self.my_options.get_text() # display purpose
        self.assertFalse(self.my_options.matches(test_snowmelt))

def main():
    unittest.main()

if __name__ == "__main__":
    main()

