import unittest
from core.swmm.options import time_steps


class OptionsTimestepTest(unittest.TestCase):
    """Test OPTIONS: Time steps"""

    def runTest(self):
        """Test OPTIONS: Time steps"""
        self.my_options = time_steps.TimeSteps()
        name = self.my_options.SECTION_NAME
        assert name == "[OPTIONS]"

        expected_text = "[OPTIONS]\n" + \
                        " SKIP_STEADY_STATE  	NO\n" + \
                        " LAT_FLOW_TOL       	5\n" + \
                        " DRY_STEP           	01:00:00\n" + \
                        " REPORT_STEP        	00:15:00\n" + \
                        " WET_STEP           	00:05:00\n" + \
                        " SYS_FLOW_TOL       	5\n" + \
                        " ROUTING_STEP       	00:05:00"

        assert self.my_options.matches(expected_text)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
