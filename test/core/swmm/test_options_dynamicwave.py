import unittest
from core.swmm.options import dynamic_wave
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match

class  OptionsDynamicWaveTest(unittest.TestCase):
    """Test OPTIONS section: Dynamic Wave"""

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
        my_options = SectionReader.read(expected_text)
        assert match(SectionWriter.as_text(my_options), expected_text)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
