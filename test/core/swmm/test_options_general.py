import unittest
from core.swmm.options.general import General, FlowRouting, FlowUnits

class OptionsGeneralTest(unittest.TestCase):
    """Test OPTIONS section
     In core.swmm.options, test field values after setting from text.
     This primarily tests General, but also tests Dates, TimeSteps, and DynamicWave since those are set from General.
    """

    TEST_TEXT = (
        ("""[OPTIONS]
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
         True),
        ("""[OPTIONS]
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
         False)
    )

    def test_all_opts(self):
        """Test all default values specified in 5.1"""
        test_all_ops = r"""[OPTIONS]
FLOW_UNITS CFS
INFILTRATION HORTON
FLOW_ROUTING KINWAVE
LINK_OFFSETS DEPTH
FORCE_MAIN_EQUATION H-W
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

        self.options = General()
        # Set_text
        self.options.set_text(test_all_ops)

        # Assert attributes
        assert self.options.flow_units == FlowUnits.CFS
        assert self.options.flow_routing == FlowRouting.KINWAVE
        assert self.options.ignore_snowmelt == False
        assert self.options.ignore_groundwater == False
        assert self.options.ignore_rdii == False
        assert self.options.dates.start_date == '1/1/2002'
        assert self.options.dates.start_time == '0:00:00'
        assert float(self.options.time_steps.system_flow_tolerance) == 5.0
        assert float(self.options.time_steps.lateral_inflow_tolerance) == 5.0
        assert self.options.temp_dir == r'.\temp'

        # Get_text
        actual_text = self.options.get_text()

        # Set_text again
        self.options.set_text(actual_text)
        assert self.options.flow_units == FlowUnits.CFS
        assert self.options.flow_routing == FlowRouting.KINWAVE
        assert self.options.ignore_snowmelt == False
        assert self.options.ignore_rdii == False
        assert self.options.dates.start_date == '1/1/2002'
        assert self.options.dates.start_time == '0:00:00'
        assert self.options.matches(test_all_ops), 'incorrect title block'

    def test_current_text(self):
        """Test setting from the current text array"""
        self.options = General()
        for current_text in self.TEST_TEXT:
            self.options.set_text(current_text[0])
            assert self.options.flow_units == current_text[1]
            assert self.options.infiltration == current_text[2]
            assert self.options.flow_routing == current_text[3]
            assert self.options.dates.start_date == current_text[4]
            assert self.options.dates.start_time == current_text[5]
            assert self.options.dates.report_start_date == current_text[6]
            assert self.options.dates.report_start_time == current_text[7]
            assert self.options.dates.end_date == current_text[8]
            assert self.options.dates.end_time == current_text[9]
            assert int(self.options.dates.dry_days) == int(current_text[10])
            assert self.options.time_steps.wet_step == current_text[11]
            assert self.options.time_steps.dry_step == current_text[12]
            assert self.options.time_steps.routing_step == current_text[13]
            assert self.options.time_steps.report_step == current_text[14]
            assert self.options.allow_ponding == current_text[15]
            assert self.options.dynamic_wave.inertial_damping.name == current_text[16]
            assert float(self.options.dynamic_wave.variable_step) == float(current_text[17])
            assert int(self.options.dynamic_wave.lengthening_step) == int(current_text[18])
            assert float(self.options.dynamic_wave.min_surface_area) == float(current_text[19])
            assert int(self.options.compatibility) == int(current_text[20])
            assert self.options.ignore_groundwater == current_text[21]

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
                        " ROUTING_STEP       	00:02:00\n"\
                        ";; Dynamic Wave\n"\
                        " LENGTHENING_STEP   	1.0\n"\
                        " VARIABLE_STEP      	0.6\n"\
                        " INERTIAL_DAMPING   	PARTIAL\n"\
                        " FORCE_MAIN_EQUATION	H-W\n"\
                        " NORMAL_FLOW_LIMITED	BOTH\n"\
                        " MAX_TRIALS         	8\n"\
                        " MIN_SURFAREA       	2.0\n"\
                        " HEAD_TOLERANCE     	0.005\n"\
                        " THREADS            	1\n"\
                        " MINIMUM_STEP       	0.5"

        self.options.set_text(expected_text)
        actual_text = self.options.get_text()
        assert self.options.matches(expected_text)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
