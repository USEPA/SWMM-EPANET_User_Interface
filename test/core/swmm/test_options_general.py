import unittest
from core.swmm.options.general import General, FlowRouting, FlowUnits
from core.swmm.inp_reader_sections import GeneralReader
from core.swmm.inp_writer_sections import GeneralWriter
from test.core.section_match import match

class OptionsGeneralTest(unittest.TestCase):
    """Test OPTIONS section
     In core.swmm.options, test field values after setting from text.
     This primarily tests General, but also tests Dates, TimeSteps, and DynamicWave since those are set from General.
    """

    TEST_TEXT = [
        ["""[OPTIONS]
 FLOW_UNITS            \tCFS
 INFILTRATION          \tHORTON
 FLOW_ROUTING          \tKW
 START_DATE            \t01/01/1998
 START_TIME            \t00:00:00
 REPORT_START_DATE     \t01/01/1998
 REPORT_START_TIME     \t00:00:00
 END_DATE              \t01/02/1998
 END_TIME              \t12:00:00
 DRY_DAYS              \t5
 WET_STEP              \t00:15:00
 DRY_STEP              \t01:00:00
 ROUTING_STEP          \t00:01:00
 REPORT_STEP           \t01:00:00
 ALLOW_PONDING         \tNO
 INERTIAL_DAMPING      \tPARTIAL
 VARIABLE_STEP         \t0.75
 LENGTHENING_STEP      \t0
 MIN_SURFAREA          \t0
 COMPATIBILITY         \t5
 IGNORE_GROUNDWATER    \tYES""",

         FlowUnits.CFS,
         "HORTON",
         FlowRouting.KINWAVE,
         "01/01/1998",
         "00:00:00",
         "01/01/1998",
         "00:00:00",
         "01/02/1998",
         "12:00:00",
         "5",
         "00:15:00",
         "01:00:00",
         "00:01:00",
         "01:00:00",
         False,
         "PARTIAL",
         "0.75",
         "0",
         "0",
         "5",
         True],
        ["""[OPTIONS]
 FLOW_UNITS            \tMGD
 INFILTRATION          \tGREEN_AMPT
 FLOW_ROUTING          \tDYNWAVE
 START_DATE            \t02/02/2000
 START_TIME            \t00:01:00
 REPORT_START_DATE     \t02/03/2000
 REPORT_START_TIME     \t00:02:00
 END_DATE              \t02/04/2000
 END_TIME              \t12:30:00
 DRY_DAYS              \t4
 WET_STEP              \t00:30:00
 DRY_STEP              \t01:30:00
 ROUTING_STEP          \t00:02:00
 REPORT_STEP           \t02:00:00
 ALLOW_PONDING         \tYES
 INERTIAL_DAMPING      \tPARTIAL
 VARIABLE_STEP         \t0.6
 LENGTHENING_STEP      \t1
 MIN_SURFAREA          \t2
 COMPATIBILITY         \t4
 IGNORE_GROUNDWATER    \tNO""",

         FlowUnits.MGD,
         "GREEN_AMPT",
         FlowRouting.DYNWAVE,
         "02/02/2000",
         "00:01:00",
         "02/03/2000",
         "00:02:00",
         "02/04/2000",
         "12:30:00",
         "4",
         "00:30:00",
         "01:30:00",
         "00:02:00",
         "02:00:00",
         True,
         "PARTIAL",
         "0.6",
         "1",
         "2",
         "4",
         False]
    ]

    def test_all_opts(self):
        """Test all default values specified in 5.1"""
        test_text = r"""[OPTIONS]
FLOW_UNITS CFS
INFILTRATION HORTON
FLOW_ROUTING KINWAVE
LINK_OFFSETS DEPTH
FORCE_MAIN_EQUATION H-W
SURCHARGE_METHOD EXTRAN
IGNORE_RAINFALL NO
IGNORE_SNOWMELT NO
IGNORE_GROUNDWATER NO
IGNORE_RDII NO
IGNORE_ROUTING NO
IGNORE_QUALITY NO
ALLOW_PONDING NO
SKIP_STEADY_STATE NO
SYS_FLOW_TOL 5
LAT_FLOW_TOL 5
START_DATE 1/1/2002
START_TIME 0:00:00
END_DATE 1/1/2002
END_TIME 24:00:00
REPORT_START_DATE 4/11/2016
REPORT_START_TIME 09:00:00
SWEEP_START 1/1
SWEEP_END 12/31
DRY_DAYS 0
REPORT_STEP 0:15:00
WET_STEP 0:05:00
DRY_STEP 1:00:00
ROUTING_STEP 600
RULE_STEP 00:00:00
LENGTHENING_STEP 0
VARIABLE_STEP 0
MINIMUM_STEP 0.5
INERTIAL_DAMPING NONE
NORMAL_FLOW_LIMITED BOTH
MIN_SURFAREA 0
MIN_SLOPE 0
MAX_TRIALS 8
HEAD_TOLERANCE 0.005
THREADS 1
TEMPDIR .\temp"""

        my_options = GeneralReader.read(test_text)
        actual_text = GeneralWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

        # Assert attributes
        assert my_options.flow_units == FlowUnits.CFS
        assert my_options.flow_routing == FlowRouting.KINWAVE
        assert my_options.ignore_snowmelt == False
        assert my_options.ignore_groundwater == False
        assert my_options.ignore_rdii == False
        assert my_options.dates.start_date == '1/1/2002'
        assert my_options.dates.start_time == '0:00:00'
        assert float(my_options.time_steps.system_flow_tolerance) == 5.0
        assert float(my_options.time_steps.lateral_inflow_tolerance) == 5.0
        assert my_options.temp_dir == r'.\temp'

        # Set_text again
        my_options2 = GeneralReader.read(actual_text)
        assert my_options2.flow_units == FlowUnits.CFS
        assert my_options2.flow_routing == FlowRouting.KINWAVE
        assert my_options2.ignore_snowmelt == False
        assert my_options2.ignore_rdii == False
        assert my_options2.dates.start_date == '1/1/2002'
        assert my_options2.dates.start_time == '0:00:00'
        actual_text2 = GeneralWriter.as_text(my_options2)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text2
        self.assertTrue(match(actual_text2, test_text), msg)

    def test_current_text(self):
        """Test setting from the current text array"""
        for current_text in self.TEST_TEXT:
            my_options = GeneralReader.read(current_text[0])
            assert my_options.flow_units == current_text[1]
            assert my_options.infiltration == current_text[2]
            assert my_options.flow_routing == current_text[3]
            assert my_options.dates.start_date == current_text[4]
            assert my_options.dates.start_time == current_text[5]
            assert my_options.dates.report_start_date == current_text[6]
            assert my_options.dates.report_start_time == current_text[7]
            assert my_options.dates.end_date == current_text[8]
            assert my_options.dates.end_time == current_text[9]
            assert int(my_options.dates.dry_days) == int(current_text[10])
            assert my_options.time_steps.wet_step == current_text[11]
            assert my_options.time_steps.dry_step == current_text[12]
            assert my_options.time_steps.routing_step == current_text[13]
            assert my_options.time_steps.report_step == current_text[14]
            assert my_options.allow_ponding == current_text[15]
            assert my_options.dynamic_wave.inertial_damping.name == current_text[16]
            assert float(my_options.dynamic_wave.variable_step) == float(current_text[17])
            assert int(my_options.dynamic_wave.lengthening_step) == int(current_text[18])
            assert float(my_options.dynamic_wave.min_surface_area) == float(current_text[19])
            assert int(my_options.compatibility) == int(current_text[20])
            assert my_options.ignore_groundwater == current_text[21]

        expected_text = "[OPTIONS]\n"\
                        " IGNORE_GROUNDWATER 	NO\n"\
                        " IGNORE_QUALITY     	NO\n"\
                        " IGNORE_ROUTING     	NO\n"\
                        " LINK_OFFSETS       	DEPTH\n"\
                        " FLOW_UNITS         	MGD\n"\
                        " MIN_SLOPE          	0.0\n"\
                        " INFILTRATION       	GREEN_AMPT\n"\
                        " ALLOW_PONDING      	YES\n"\
                        " IGNORE_SNOWMELT    	NO\n"\
                        " IGNORE_RDII        	NO\n"\
                        " IGNORE_RAINFALL    	NO\n"\
                        " COMPATIBILITY      	4\n"\
                        " FLOW_ROUTING       	DYNWAVE\n"\
                        ";; Dates\n"\
                        " END_TIME           	12:30:00\n"\
                        " END_DATE           	02/04/2000\n"\
                        " SWEEP_END          	12/31\n"\
                        " START_TIME         	00:01:00\n"\
                        " DRY_DAYS           	4\n"\
                        " REPORT_START_TIME  	00:02:00\n"\
                        " START_DATE         	02/02/2000\n"\
                        " SWEEP_START        	1/1\n"\
                        " REPORT_START_DATE  	02/03/2000\n"\
                        ";; Time Steps\n"\
                        " SKIP_STEADY_STATE  	NO\n"\
                        " LAT_FLOW_TOL       	5\n"\
                        " DRY_STEP           	01:30:00\n"\
                        " REPORT_STEP        	02:00:00\n"\
                        " WET_STEP           	00:30:00\n"\
                        " SYS_FLOW_TOL       	5\n"\
                        " ROUTING_STEP       	00:02:00\n" \
                        " RULE_STEP             00:00:00\n" \
                        ";; Dynamic Wave\n"\
                        " LENGTHENING_STEP   	1.0\n"\
                        " VARIABLE_STEP      	0.6\n"\
                        " INERTIAL_DAMPING   	PARTIAL\n"\
                        " FORCE_MAIN_EQUATION	H-W\n" \
                        " SURCHARGE_METHOD      EXTRAN\n"\
                        " NORMAL_FLOW_LIMITED	BOTH\n"\
                        " MAX_TRIALS         	8\n"\
                        " MIN_SURFAREA       	2.0\n"\
                        " HEAD_TOLERANCE     	0.005\n"\
                        " THREADS            	1\n"\
                        " MINIMUM_STEP       	0.5"

        my_options = GeneralReader.read(expected_text)
        actual_text = GeneralWriter.as_text(my_options)
        msg = '\nSet:' + expected_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, expected_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
