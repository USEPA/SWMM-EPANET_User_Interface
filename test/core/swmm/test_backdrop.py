import unittest
from core.swmm.options.backdrop import BackdropOptions
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match

class SimpleBackdropTest(unittest.TestCase):
    """Test BACKDROP section"""

    def test_bare(self):
        """Test bare section"""
        self.my_options = BackdropOptions()
        default_text = BackdropOptionsWriter.as_text(self.my_options)
        test_text = "[BACKDROP]"
        self.my_options = BackdropOptionsReader.read(test_text)
        actual_text = BackdropOptionsWriter.as_text(self.my_options)
        assert actual_text == default_text

    def test_backdrop(self):
        """Test backdrop parameters"""
        self.my_options = BackdropOptions()
        test_text = """[BACKDROP]
        DIMENSIONS    0.0	  0.0	0.0	 0.0
         """
        self.my_options = BackdropOptionsReader.read(test_text)
        actual_text = BackdropOptionsWriter.as_text(self.my_options)
        assert match(actual_text, test_text)

    def test_missing_value(self): # TODO test missing value causes a crash
        """Test on missing value"""
        test_text = """[BACKDROP]
        DIMENSIONS     0.0     0.0     0.0
         """
        self.my_options = BackdropOptionsReader.read(test_text)
        # self.assertFalse(self.my_options.matches(test_text))
