from core.swmm.options.backdrop import BackdropOptions
from core.swmm.options import backdrop
import unittest


class  OptionsBackdropTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_options = BackdropOptions()

    def setUp(self):

        self.my_backdrop = backdrop.BackdropOptions()


    def runTest(self):

        name = self.my_backdrop.SECTION_NAME
        assert name == "[BACKDROP]"

        expected_text = "[BACKDROP]\n" + \
                        " DIMENSIONS       	             0.0	             0.0	             0.0	             0.0"

        actual_text = self.my_backdrop.get_text()
        assert actual_text == expected_text
