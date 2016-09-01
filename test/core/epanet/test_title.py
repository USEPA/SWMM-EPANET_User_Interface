from core.epanet.title import Title
from core.epanet.inp_reader_sections import TitleReader
from core.epanet.inp_writer_sections import TitleWriter
from test.core.section_match import match
import unittest


class SimpleTitleTest(unittest.TestCase):
    """Test Title section"""

    def test_bare(self):
        """Bare section"""
        my_title = Title()
        # default_text = self.my_title.get_text()
        default_text = TitleWriter.as_text(my_title)

        test_text = ""
        # self.my_title.set_text(test_text)
        my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(my_title)
        # assert actual_text == test_text
        assert actual_text == default_text

    def test_empty(self):
        """Empty section (has section name)"""
        test_text = "[TITLE]\n"
        my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(my_title)
        # assert self.my_title.matches(test_text)
        assert match(actual_text, test_text)

    def test_one_row(self):
        """One-row title with carriage return"""
        test_text = "[TITLE]\n" \
                    "test_title\n"
        my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(my_title)
        assert match(actual_text, test_text)

    def test_multi_row(self):
        """Multiple-row title include empty lines"""
        test_text = "[TITLE]\n" \
                    "       \n" \
                    "test_title\n" \
                    "    "
        my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(my_title)
        assert match(actual_text, test_text)

    def test_rt_before_title(self):
        """Carriage return before section title"""
        # The first row can not be \n
        test_text = "\n"\
                    "[TITLE]\n"\
                    "test_title"
        my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(my_title)
        assert match(actual_text, test_text)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

