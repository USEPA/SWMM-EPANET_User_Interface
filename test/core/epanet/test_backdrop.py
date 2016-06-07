import unittest
from core.epanet.options.options import Options
from core.epanet.options import backdrop


class SimpleBackdropTest(unittest.TestCase):
    """Test Backdrop section"""

    def runTest(self):
        my_backdrop = backdrop.BackdropOptions()
        assert my_backdrop.SECTION_NAME == "[BACKDROP]"

        my_backdrop.file = "BackdropFilename"

        expected_text = "[BACKDROP]\n" \
                        "FILE BackdropFilename\n" \
                        "DIMENSIONS 0.0 0.0 10000.0 10000.0\n" \
                        "UNITS NONE\n" \
                        "OFFSET 0.0 0.0"

        assert my_backdrop.matches(expected_text)

        my_backdrop.dimensions = ("1.0", "2.0", "30000.0", "40000.0")
        my_backdrop.units = backdrop.BackdropUnits.METERS
        my_backdrop.offset = ("1.1", "2.2")

        expected_text = "[BACKDROP]\n" \
                        "FILE BackdropFilename\n" \
                        "DIMENSIONS 1.0 2.0 30000.0 40000.0\n" \
                        "UNITS METERS\n" \
                        "OFFSET 1.1 2.2"

        assert my_backdrop.matches(expected_text)
