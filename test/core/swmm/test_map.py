import unittest
from core.swmm.options.map import MapOptions
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match


class SimpleMapTest(unittest.TestCase):
    """Test MAP section"""

    TEST_TEXTS = [("[MAP]\n"
                  "DIMENSIONS 0.000 0.000 10000.000 10000.000\n"
                  "Units      None")]

    def test_writer(self):
        """Test MapOptionsWriter"""
        my_options = MapOptions()
        name = my_options.SECTION_NAME
        assert name == "[MAP]"

        test_text = "[MAP]\n" + \
                    " DIMENSIONS 0.0 0.0 0.0 0.0\n" + \
                    " UNITS            \tNONE"
        actual_text = MapOptionsWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_reader(self):
        """Test MapOptionsReaderWriter"""
        for test_text in self.TEST_TEXTS:
            my_options = MapOptionsReader.read(test_text)
            mapxy = []
            for s in test_text.split():
                if s.isdigit():
                    mapxy.append(float(s))
            for i in range(len(mapxy)):
                assert my_options.dimensions[i] == mapxy[i]
            actual_text = MapOptionsWriter.as_text(my_options)
            msg = '\nSet:' + test_text + '\nGet:' + actual_text
            self.assertTrue(match(actual_text, test_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
