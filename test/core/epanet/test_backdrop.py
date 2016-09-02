import unittest
from core.epanet.options.options import Options
from core.epanet.options import backdrop
from core.epanet.inp_reader_sections import BackdropOptionsReader
from core.epanet.inp_writer_sections import BackdropOptionsWriter
from test.core.section_match import match


class SimpleBackdropTest(unittest.TestCase):
    """Test Backdrop section"""

    def test_writer(self):
        """Test BackdropOptionsWriter by specify attributes"""
        my_backdrop = backdrop.BackdropOptions()
        assert my_backdrop.SECTION_NAME == "[BACKDROP]"

        my_backdrop.file = "BackdropFilename"

        expected_text = "[BACKDROP]\n" \
                        "FILE BackdropFilename\n" \
                        "DIMENSIONS 0.0 0.0 10000.0 10000.0\n" \
                        "UNITS NONE\n" \
                        "OFFSET 0.0 0.0"

        actual_text = BackdropOptionsWriter.as_text(my_backdrop)
        msg = '\nSet:'+expected_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, expected_text), msg)

        my_backdrop.dimensions = ("1.0", "2.0", "30000.0", "40000.0")
        my_backdrop.units = backdrop.BackdropUnits.METERS
        my_backdrop.offset = ("1.1", "2.2")

        expected_text = "[BACKDROP]\n" \
                        "FILE BackdropFilename\n" \
                        "DIMENSIONS 1.0 2.0 30000.0 40000.0\n" \
                        "UNITS METERS\n" \
                        "OFFSET 1.1 2.2"

        actual_text = BackdropOptionsWriter.as_text(my_backdrop)
        msg = '\nSet:'+expected_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, expected_text), msg)

    def test_reader(self):
        """Test BackdropOptionsReader by reading from file"""
        test_text = "[BACKDROP]\n" \
                    "FILE BackdropFilename\n" \
                    "DIMENSIONS 0.0 0.0 10000.0 10000.0\n" \
                    "UNITS NONE\n" \
                    "OFFSET 0.0 0.0"
        my_backdrop = BackdropOptionsReader.read(test_text)
        actual_text = BackdropOptionsWriter.as_text(my_backdrop)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
