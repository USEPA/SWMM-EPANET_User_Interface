import unittest
from core.swmm.title import Title


class SimpleTitleTest(unittest.TestCase):
    """Test TITLE section"""

    def test_bare(self):
        """Bare section read/write"""
        self.my_title = Title()
        default_text = self.my_title.get_text()
        test_text = ""
        self.my_title.set_text(test_text)
        actual_text = self.my_title.get_text()
        assert actual_text == default_text

    def test_empty(self):
        """Empty section read/write"""
        test_text = "[TITLE]\n"
        self.my_title = Title()
        self.my_title.set_text(test_text)
        actual_text = self.my_title.get_text()  # display purpose
        assert self.my_title.matches(test_text)

    def test_empty_wo_return(self):
        """Empty section read/write wo ending carriage return"""
        test_text = "[TITLE]"
        self.my_title = Title()
        self.my_title.set_text(test_text)
        actual_text = self.my_title.get_text()  # display purpose
        assert self.my_title.matches(test_text)

    def test_one_row_wt_return(self):
        """One-row title wt ending carriage return"""
        test_text = "[TITLE]\n" \
                    "test_title\n"
        self.my_title = Title()
        self.my_title.set_text(test_text)
        actual_text = self.my_title.get_text()  # display purpose
        assert self.my_title.matches(test_text)

    def test_multiple_lines(self):
        """Test multiple lines with empty lines"""
        test_text = r"""[TITLE]

                test_title

                """
        self.my_title = Title()
        self.my_title.set_text(test_text)
        actual_text = self.my_title.get_text()  # display purpose
        assert self.my_title.matches(test_text)

    def test_return_before_title(self):
        """Carriage return before Section title"""
        test_text = "\n"\
                    "[TITLE]\n"\
                    "test_title"
        self.my_title = Title()
        self.my_title.set_text(test_text)
        actual_text = self.my_title.get_text()  # display purpose
        assert self.my_title.matches(test_text)