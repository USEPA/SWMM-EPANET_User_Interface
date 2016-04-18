from core.swmm.options.backdrop import BackdropOptions
import unittest


class  SimpleBackdropTest(unittest.TestCase):

    def setUp(self):
        self.my_options = BackdropOptions()

    def runTest(self):

        # Test default, default is empty string
        # Test failed as empty string is not produced by get_text()
        name = self.my_options.SECTION_NAME
        assert name == "[BACKDROP]"
        actual_text = self.my_options.get_text()
        assert actual_text == ''

        # Test one set of parameters
        # --Test set_text
        backdrop_options = """
        [BACKDROP]
        DIMENSIONS       	             0.0	             0.0	             0.0	             0.0
         """
        self.my_options.set_text(backdrop_options)
        actual_text = self.my_options.get_text()
        # --Test get_text through matches
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(backdrop_options)
        pass
