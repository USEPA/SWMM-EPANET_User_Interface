import unittest
from core.swmm.options import dynamic_wave
from core.swmm.options.dynamic_wave import InertialDamping, ForceMainEquation, NormalFlowLimited
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match

class  OptionsDynamicWaveTest(unittest.TestCase):
    """Test OPTIONS section: Dynamic Wave"""

    def runTest(self):
        """Test OPTIONS: Dynamic Wave """
        expected_text = "[OPTIONS]\n" + \
                        " LENGTHENING_STEP   	0.0\n" + \
                        " VARIABLE_STEP      	0.0\n" + \
                        " INERTIAL_DAMPING   	NONE\n" + \
                        " FORCE_MAIN_EQUATION	H_W\n" + \
                        " NORMAL_FLOW_LIMITED	BOTH\n" + \
                        " MAX_TRIALS         	8\n" + \
                        " MIN_SURFAREA       	0.0\n" + \
                        " HEAD_TOLERANCE     	0.005\n" + \
                        " THREADS            	1\n" + \
                        " MINIMUM_STEP       	0.5"


        # Test example from expected_text
        my_options = GeneralReader.read(expected_text)
        assert my_options.dynamic_wave.lengthening_step == "0.0"
        assert my_options.dynamic_wave.variable_step == "0.0"
        assert my_options.dynamic_wave.inertial_damping == InertialDamping.NONE
        assert my_options.dynamic_wave.force_main_equation == ForceMainEquation.H_W
        assert my_options.dynamic_wave.normal_flow_limited == NormalFlowLimited.BOTH
        assert my_options.dynamic_wave.max_trials == "8"
        assert my_options.dynamic_wave.min_surface_area == "0.0"
        assert my_options.dynamic_wave.head_tolerance == "0.005"
        assert my_options.dynamic_wave.threads == "1"
        assert my_options.dynamic_wave.minimum_step == "0.5"

        # actual_text = GeneralWriter.as_text(my_options)
        # msg = '\nSet:' + expected_text + '\nGet:' + actual_text
        # self.assertTrue(match(actual_text, expected_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
