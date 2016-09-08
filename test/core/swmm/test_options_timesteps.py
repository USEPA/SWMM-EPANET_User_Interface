import unittest
from core.swmm.options import time_steps
from core.swmm.inp_reader_sections import GeneralReader
from core.swmm.inp_writer_sections import GeneralWriter
from test.core.section_match import match


class OptionsTimestepTest(unittest.TestCase):
    """Test OPTIONS: Time steps"""

    def runTest(self):
        """Test OPTIONS: Time steps"""
        my_options = time_steps.TimeSteps()
        name = my_options.SECTION_NAME
        assert name == "[OPTIONS]"

        expected_text = "[OPTIONS]\n" + \
                        " SKIP_STEADY_STATE  	NO\n" + \
                        " LAT_FLOW_TOL       	5\n" + \
                        " DRY_STEP           	01:00:00\n" + \
                        " REPORT_STEP        	00:15:00\n" + \
                        " WET_STEP           	00:05:00\n" + \
                        " SYS_FLOW_TOL       	5\n" + \
                        " ROUTING_STEP       	00:05:00"

        my_options = GeneralReader.read(expected_text)
        assert my_options.time_steps.skip_steady_state == False
        assert my_options.time_steps.lateral_inflow_tolerance == "5"
        assert my_options.time_steps.dry_step == "01:00:00"
        assert my_options.time_steps.report_step == "00:15:00"
        assert my_options.time_steps.wet_step == "00:05:00"
        assert my_options.time_steps.system_flow_tolerance == "5"
        assert my_options.time_steps.routing_step == "00:05:00"
        # actual_text = GeneralWriter.as_text(my_options)
        # msg = '\nSet:' + expected_text + '\nGet:' + actual_text
        # self.assertTrue(match(actual_text, expected_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
