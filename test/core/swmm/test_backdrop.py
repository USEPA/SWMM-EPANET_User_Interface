import unittest
from core.swmm.options.backdrop import BackdropOptions


class SimpleBackdropTest(unittest.TestCase):
    """Test BACKDROP section"""

    def test_bare(self):
        """Test bare section"""
        self.my_options = BackdropOptions()
        default_text = self.my_options.get_text()
        test_text = "[BACKDROP]"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()
        assert actual_text == default_text

    def test_backdrop(self):
        """Test backdrop parameters"""
        self.my_options = BackdropOptions()
        test_text = """[BACKDROP]
        DIMENSIONS    0.0	  0.0	0.0	 0.0
         """
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_text)

    def test_missing_value(self): # TODO test missing value causes a crash
        """Test on missing value"""
        self.my_options = BackdropOptions()
        test_text = """[BACKDROP]
        DIMENSIONS     0.0     0.0     0.0
         """
        self.my_options.set_text(test_text)
        # self.assertFalse(self.my_options.matches(test_text))