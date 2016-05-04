from core.swmm.title import Title
import unittest


class SimpleTitleTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):
        self.my_title = Title()

    def runTest(self):

        default_text = self.my_title.get_text()

        # Bare section read/write
        test_text = r"""[TITLE]"""
        # --Test set_text
        self.my_title.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_title.get_text()  # display purpose
        # assert self.my_title.matches(test_text)
        assert actual_text == default_text

        # Test title
        # Normal one row title
        test_text = r"""[TITLE]
        Test Title
        """
        # --Test set_text
        self.my_title.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_title.get_text()  # display purpose
        assert self.my_title.matches(test_text)


        # Multiple lines with empty lines
        test_text = r"""[TITLE]

        test_title

        test this title
        """
        # --Test set_text
        self.my_title.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_title.get_text()  # display purpose
        assert self.my_title.matches(test_text)

        # Empty first row before Section title
        # ---- Failed as the first row can not be \n
        test_text = r"""
        [TITLE]
        test_title
        """
        # --Test set_text
        self.my_title.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_title.get_text()  # display purpose
        assert self.my_title.matches(test_text)

        pass


