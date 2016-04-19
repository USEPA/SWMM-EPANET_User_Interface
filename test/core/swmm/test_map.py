from core.swmm.options.map import MapOptions
import unittest


class SimpleMapTest(unittest.TestCase):

    TEST_TEXT = [("[MAP]\n"
                  "DIMENSIONS 0.000 0.000 10000.000 10000.000\n"
                  "Units      None")]

    def setUp(self):

        self.my_options = MapOptions()

    def runTest(self):

        name = self.my_options.SECTION_NAME
        assert name == "[MAP]"

        expected_text = "[MAP]\n" + \
                        " DIMENSIONS 0.0 0.0 0.0 0.0\n" + \
                        " UNITS            \tNONE"

        assert self.my_options.matches(expected_text)

        for current_map_option in self.TEST_TEXT:
            self.my_options.set_text(current_map_option)
            mapxy = []
            for s in current_map_option.split():
                if s.isdigit():
                    mapxy.append(float(s))
            for i in range(len(mapxy)):
                assert self.my_options.dimensions[i] == mapxy[i]
        pass


