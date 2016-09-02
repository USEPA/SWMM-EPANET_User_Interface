import unittest
from core.epanet.options import times
from core.epanet.inp_reader_sections import TimesOptionsReader()
from core.epanet.inp_writer_sections import TimesOptionsWriter()
from test.core.section_match import match


class SimpleTimesTest(unittest.TestCase):
    """Test Times section"""

    def test_no_leading_space(self):
        """Case 1. data from Net1.inp
        No leading white spaces in input texts"""
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
        my_times  = TimesOptionsReader.read(test_text)
        actual_text = TimesOptionsWriter.as_text(my_times)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_leading_space(self):
        """Case 2. data from Net1.inp
        With leading white spaces in input texts"""
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
        my_times  = TimesOptionsReader.read(test_text)
        actual_text = TimesOptionsWriter.as_text(my_times)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_get(self):
        """Test get_text"""
        my_times = times.TimesOptions()
        my_times.duration = "24:00"
        my_times.hydraulic_timestep = "1:00"	    # hours:minutes
        my_times.quality_timestep = "0:05"		    # hours:minutes
        my_times.rule_timestep = "0:05" 		    # hours:minutes
        my_times.pattern_timestep = "1:00" 		    # hours:minutes
        my_times.pattern_start = "0:00"	            # hours:minutes
        my_times.report_timestep = "1:00"		    # hours:minutes
        my_times.report_start = "0:00"	            # hours:minutes
        my_times.start_clocktime = "12 am"		    # hours:minutes AM/PM
        my_times.statistic = times.StatisticOptions.AVERAGED  # NONE/AVERAGED/MINIMUM/MAXIMUM/RANGE

        name = my_times.SECTION_NAME
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

        actual_text = TimesOptionsWriter.as_text(my_times)
        msg = '\nSet:'+expected_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, expected_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
