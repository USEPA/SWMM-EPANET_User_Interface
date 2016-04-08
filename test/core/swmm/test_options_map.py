from core.swmm.options.map import MapOptions
from core.swmm.options import map
import unittest


class OptionsMapTest(unittest.TestCase):
    TEST_TEXT = (("""[MAP]
                DIMENSIONS 0.000 0.000 10000.000 10000.000
                Units      None"""))

    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_options = MapOptions()

    def setUp(self):

        self.my_options = map.MapOptions()


    def runTest(self):

        name = self.my_options.SECTION_NAME
        assert name == "[MAP]"

        expected_text = "[MAP]\n" + \
                        " DIMENSIONS       \t" + \
                        "             0.0\t" + \
                        "             0.0\t" + \
                        "             0.0\t" + \
                        "             0.0\n" + \
                        " UNITS            \t" + \
                        "NONE"

        actual_text = self.my_options.get_text()
        assert actual_text == expected_text

        #20160407xw: Test set_text, currently fail because the format is not tab delimited.
        for current_map_option in self.TEST_TEXT:
            self.my_options.set_text(current_map_option)
            mapxy = []
            for s in current_map_option.split():
                if s.isdigit():
                    mapxy.append(float(s))
            for i in range(len(mapxy)):
                assert self.my_options.dimensions[i] == mapxy[i]
        pass


