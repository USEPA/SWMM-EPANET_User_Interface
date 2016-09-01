import unittest
from core.swmm.title import Title
from core.swmm.inp_reader_sections import TitleReader
from core.swmm.inp_writer_sections import TitleWriter
from test.core.section_match import match


class SimpleTitleTest(unittest.TestCase):
    """Test TITLE section"""

    def test_bare(self):
        """Bare section read/write"""
        self.my_title = Title()
        default_text = TitleWriter.as_text(self.my_title)
        test_text = ""
        self.my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(self.my_title)
        assert actual_text == default_text

    def test_empty(self):
        """Empty section read/write"""
        test_text = "[TITLE]\n"
        self.my_title = Title()
        self.my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(self.my_title)
        assert match(actual_text, test_text)

    def test_empty_wo_return(self):
        """Empty section read/write wo ending carriage return"""
        test_text = "[TITLE]"
        self.my_title = Title()
        self.my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(self.my_title)
        assert match(actual_text, test_text)

    def test_one_row_wt_return(self):
        """One-row title wt ending carriage return"""
        test_text = "[TITLE]\n" \
                    "test_title\n"
        self.my_title = Title()
        self.my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(self.my_title)
        assert match(actual_text, test_text)

    def test_multiple_lines(self):
        """Test multiple lines with empty lines"""
        test_text = r"""[TITLE]

                test_title

                """
        self.my_title = Title()
        self.my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(self.my_title)
        assert match(actual_text, test_text)

    def test_return_before_title(self):
        """Carriage return before Section title"""
        test_text = "\n"\
                    "[TITLE]\n"\
                    "test_title"
        self.my_title = Title()
        self.my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(self.my_title)
        assert match(actual_text, test_text)

def main():
    unittest.main()

if __name__ == "__main__":
    main()