import unittest
from core.swmm.options import dynamic_wave


class  OptionsDynamicWaveTest(unittest.TestCase):
    """Test OPTIONS section: Dynamic Wave"""
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = dynamic_wave.DynamicWave()

    def runTest(self):
        """Test OPTIONS: Dynamic Wave """
        name = self.my_options.SECTION_NAME
        assert name == "[OPTIONS]"

        expected_text = "[OPTIONS]\n" + \
                        " LENGTHENING_STEP   	0.0\n" + \
                        " VARIABLE_STEP      	0.0\n" + \
                        " INERTIAL_DAMPING   	NONE\n" + \
                        " FORCE_MAIN_EQUATION	H-W\n" + \
                        " NORMAL_FLOW_LIMITED	BOTH\n" + \
                        " MAX_TRIALS         	8\n" + \
                        " MIN_SURFAREA       	0.0\n" + \
                        " HEAD_TOLERANCE     	0.005\n" + \
                        " THREADS            	1\n" + \
                        " MINIMUM_STEP       	0.5"


        # Test example from expected_text
        test_text = expected_text
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)
