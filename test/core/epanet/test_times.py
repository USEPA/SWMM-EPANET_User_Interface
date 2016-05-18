from core.epanet.options.options import Options
from core.epanet.options import times
import unittest


class SimpleTimesTest2(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):
        self.my_options = times.TimesOptions()

    def runTest(self):
        # Case 1. data from Net1.inp
        # No white spaces in input texts
        test_text = "[TIMES]\n" \
                    "Duration\t24:00\n" \
                    "Hydraulic Timestep\t1:00\n" \
                    "Quality Timestep\t0:05\n" \
                    "Rule Timestep\t0:05\n" \
                    "Pattern Timestep\t2:00\n" \
                    "Pattern Start\t0:00\n" \
                    "Report Timestep\t1:00\n" \
                    "Report Start\t0:00\n" \
                    "Start ClockTime\t12 am\n" \
                    "Statistic\tNone"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()
        # assert nw_actual_text == nw_test_text
        assert self.my_options.matches(test_text)
        pass

        # data from Net1.inp
        test_text = " [TIMES]\n" \
                    "     Duration           	24:00\n" \
                    "     Hydraulic Timestep 	1:00\n" \
                    "     Quality Timestep   	0:05\n" \
                    "     Rule Timestep      	0:05\n" \
                    "     Pattern Timestep   	2:00\n" \
                    "     Pattern Start      	0:00\n" \
                    "     Report Timestep    	1:00\n" \
                    "     Report Start       	0:00\n" \
                    "     Start ClockTime    	12 am\n" \
                    "     Statistic          	None"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()
        assert self.my_options.matches(test_text)
        pass


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

        assert self.my_times.matches(expected_text)
