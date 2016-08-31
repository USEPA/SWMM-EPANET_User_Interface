from core.epanet.title import Title
from core.epanet.inp_reader_sections import TitleReader
from core.epanet.inp_writer_sections import TitleWriter
from test.core.section_match import match
import unittest


class SimpleTitleTest(unittest.TestCase):
    """Test Title section"""

    def setUp(self):
        """Set up test"""

    def test_bare(self):
        """Bare section"""
        self.my_title = Title()
        # default_text = self.my_title.get_text()
        default_text = TitleWriter.as_text(self.my_title)

        test_text = ""
        # self.my_title.set_text(test_text)
        self.my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(self.my_title)
        # assert actual_text == test_text
        assert actual_text == default_text

    def test_empty(self):
        """Empty section (has section name)"""
        self.my_title = Title()
        test_text = "[TITLE]\n"
        self.my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(self.my_title)
        # assert self.my_title.matches(test_text)
        assert match(actual_text, test_text)

    def test_one_row(self):
        """One-row title with carriage return"""
        self.my_title = Title()
        test_text = "[TITLE]\n" \
                    "test_title\n"
        self.my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(self.my_title)
        assert match(actual_text, test_text)

    def test_multi_row(self):
        """Multiple-row title include empty lines"""
        self.my_title = Title()
        test_text = "[TITLE]\n" \
                    "       \n" \
                    "test_title\n" \
                    "    "
        self.my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(self.my_title)
        assert match(actual_text, test_text)

    def test_rt_before_title(self):
        """Carriage return before section title"""
        # The first row can not be \n
        self.my_title = Title()
        test_text = "\n"\
                    "[TITLE]\n"\
                    "test_title"
        self.my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(self.my_title)
        assert match(actual_text, test_text)
