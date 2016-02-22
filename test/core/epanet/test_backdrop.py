from core.epanet.options.options import Options
from core.epanet.options import backdrop
import unittest


class SimpleBackdropTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_options = Options()

    def setUp(self):

        self.my_backdrop = backdrop.BackdropOptions()


    def runTest(self):

        name = self.my_backdrop.SECTION_NAME
        assert name == "[BACKDROP]"

        expected_text = "[BACKDROP]\n" + \
                        " DIMENSIONS       	             0.0	             0.0	         10000.0	         10000.0\n" + \
                        " UNITS            	NONE\n" + \
                        " OFFSET           	        0.000000	        0.000000"

        actual_text = self.my_backdrop.get_text()
        assert actual_text == expected_text
