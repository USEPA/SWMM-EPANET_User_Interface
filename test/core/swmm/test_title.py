import unittest
from core.swmm.title import Title
from core.swmm.inp_reader_sections import TitleReader
from core.swmm.inp_writer_sections import TitleWriter
from test.core.section_match import match


class SimpleTitleTest(unittest.TestCase):
    """Test TITLE section"""

    def test_bare(self):
        """Bare section read/write"""
        my_title = Title()
        default_text = TitleWriter.as_text(my_title)
        test_text = "[TITLE]"
        my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(my_title)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_empty(self):
        """Empty section read/write"""
        test_text = "[TITLE]\n"
        my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(my_title)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_empty_wo_return(self):
        """Empty section read/write wo ending carriage return"""
        test_text = "[TITLE]"
        my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(my_title)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_one_row_wt_return(self):
        """One-row title wt ending carriage return"""
        test_text = "[TITLE]\n" \
                    "test_title\n"
        my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(my_title)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_multiple_lines(self):
        """Test multiple lines with empty lines"""
        test_text = r"""[TITLE]

                test_title

                """
        my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(my_title)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_return_before_title(self):
        """Carriage return before Section title"""
        test_text = "\n"\
                    "[TITLE]\n"\
                    "test_title"
        my_title = TitleReader.read(test_text)
        actual_text = TitleWriter.as_text(my_title)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()