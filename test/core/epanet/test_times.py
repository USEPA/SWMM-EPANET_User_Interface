from core.epanet.options.options import Options
from core.epanet.options import times
import unittest


class SimpleTimesTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_options = Options()

    def setUp(self):

        self.my_times = times.TimesOptions()
        self.my_times.duration = "24:00"
        self.my_times.hydraulic_timestep = "1:00"	    # hours:minutes
        self.my_times.quality_timestep = "0:05"		    # hours:minutes
        self.my_times.rule_timestep = "0:05" 		    # hours:minutes
        self.my_times.pattern_timestep = "1:00" 		    # hours:minutes
        self.my_times.pattern_start = "0:00"	            # hours:minutes
        self.my_times.report_timestep = "1:00"		    # hours:minutes
        self.my_times.report_start = "0:00"	            # hours:minutes
        self.my_times.start_clocktime = "12 am"		    # hours:minutes AM/PM
        self.my_times.statistic = times.StatisticOptions.AVERAGED  # NONE/AVERAGED/MINIMUM/MAXIMUM/RANGE

    def runTest(self):

        name = self.my_times.SECTION_NAME
        assert name == "[TIMES]"

        expected_text = "[TIMES]\n" + \
                        " Report Start       	0:00\n" + \
                        " Quality Timestep   	0:05\n" + \
                        " Report Timestep    	1:00\n" + \
                        " Hydraulic Timestep 	1:00\n" + \
                        " Pattern Timestep   	1:00\n" + \
                        " Duration           	24:00\n" + \
                        " Start ClockTime    	12 am\n" + \
                        " Statistic          	AVERAGED\n" + \
                        " Pattern Start      	0:00\n" + \
                        " Rule Timestep      	0:05"

        actual_text = self.my_times.get_text()
        assert actual_text == expected_text
