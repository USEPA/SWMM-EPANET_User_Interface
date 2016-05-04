from core.swmm.options.backdrop import BackdropOptions
import unittest


class SimpleBackdropTest(unittest.TestCase):

    def setUp(self):
        self.my_options = BackdropOptions()

    def runTest(self):

        # Get defaults
        default_text = self.my_options.get_text()

        # Bare section read/write
        # Write defaults rather than bare section, passed
        test_text = r"""[BACKDROP]"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert actual_text == default_text

        # Test one set of parameters
        test_text = """
        [BACKDROP]
        DIMENSIONS       	             0.0	             0.0	             0.0	             0.0
         """
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()
        # --Test get_text through matches
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_text)

        # Test on missing value
        # Failed test
        test_text = """
        [BACKDROP]
        DIMENSIONS       	             0.0	             0.0	             0.0
         """
        #self.my_options.set_text(test_text)

        pass
