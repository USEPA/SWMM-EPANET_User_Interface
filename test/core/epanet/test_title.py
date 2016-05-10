from core.epanet.title import Title
import unittest


class SimpleTitleTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):
        self.my_title = Title()

    def runTest(self):

        # Bare section read/write
        default_text = self.my_title.get_text()
        test_text = ""
        self.my_title.set_text(test_text)
        actual_text = self.my_title.get_text()
        # assert actual_text == test_text
        assert actual_text == default_text
        # assert self.my_title.matches(test_text)

        # Empty section read/write
        test_text = "[TITLE]\n"
        self.my_title.set_text(test_text)
        actual_text = self.my_title.get_text()  # display purpose
        assert self.my_title.matches(test_text)

        # Empty section read/write wo ending \n
        test_text = "[TITLE]"
        self.my_title.set_text(test_text)
        actual_text = self.my_title.get_text()  # display purpose
        assert self.my_title.matches(test_text)

        # One-row title wt ending \n
        test_text = "[TITLE]\n" \
                    "test_title\n"
        self.my_title.set_text(test_text)
        actual_text = self.my_title.get_text()  # display purpose
        assert self.my_title.matches(test_text)

        # Multiple lines with empty lines
        test_text = r"""[TITLE]
                test_title
                """
        self.my_title.set_text(test_text)
        actual_text = self.my_title.get_text()  # display purpose
        assert self.my_title.matches(test_text)

        # Multiple lines with empty lines
        test_text = r"""[TITLE]
                test_title

                """
        self.my_title.set_text(test_text)
        actual_text = self.my_title.get_text()  # display purpose
        assert self.my_title.matches(test_text)

        # Multiple lines with empty lines
        test_text = r"""[TITLE]

                test_title

                """
        self.my_title.set_text(test_text)
        actual_text = self.my_title.get_text()  # display purpose
        assert self.my_title.matches(test_text)

        # \n before Section title
        # The first row can not be \n
        test_text = "\n"\
                    "[TITLE]\n"\
                    "test_title"
        self.my_title.set_text(test_text)
        actual_text = self.my_title.get_text()  # display purpose
        assert self.my_title.matches(test_text)
        pass




