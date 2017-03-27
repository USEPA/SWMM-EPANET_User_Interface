import unittest
from core.swmm.hydraulics.node import Divider
from core.swmm.inp_reader_sections import DividerReader
from core.swmm.inp_writer_sections import DividerWriter
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit, match_keyword_lines


class SimpleDividerTest(unittest.TestCase):
    """Test DIVIDER section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_overflow_divider(self):
        """Test divider: OVERFLOW created according to Manual
         Name Elev DivLink OVERFLOW (Ymax Y0 Ysur Apond)
         """
        test_text = "NODE10   0      LK1    OVERFLOW   0      0     0     0"
        my_options = DividerReader.read(test_text)
        actual_text = DividerWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)
        assert my_options.name == 'NODE10'
        assert my_options.elevation == '0'
        assert my_options.diverted_link == 'LK1'
        assert my_options.max_depth == '0'
        assert my_options.initial_depth == '0'
        assert my_options.surcharge_depth == '0'
        assert my_options.ponded_area == '0'

    def test_cutoff_divider(self):
        """Test divider: CUTOFF created according to Manual
         Name Elev DivLink CUTOFF Qmin (Ymax Y0 Ysur Apond)
         """
        # test_text = "NODE10   0      LK1    OVERFLOW   0       0      0     0     0"
        test_text = "NODE10   0      LK1    CUTOFF   1       2      3     4     5"
        my_options = DividerReader.read(test_text)
        actual_text = DividerWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        # self.assertTrue(match(actual_text, test_text), msg)
        self.assertTrue(match(actual_text, test_text), msg)

    def test_tabular_divider(self):
        """Test divider: TABULAR created according to Manual
        Name Elev DivLink TABULAR Dcurve (Ymax Y0 Ysur Apond)
        """
        test_text = "NODE10   0      LK1    TABULAR   DC0       0      0     0     0"
        my_options = DividerReader.read(test_text)
        actual_text = DividerWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_weir_divider(self):
        """Test divider: WEIR created according to Manual
         Name Elev DivLink WEIR Qmin Ht Cd (Ymax Y0 Ysur Apond)
         """
        test_text = "NODE10   0      LK1    WEIR   0.5   2   0.7    2    0     0"
        my_options = DividerReader.read(test_text)
        actual_text = DividerWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match_keyword_lines(test_text, actual_text,
                                            keywords_=None, skipped_keywords=None, ignore_trailing_0=True), msg)

    def test_dividers(self):
        """Test DIVIDERS section from Example-1b"""
        source_text = "[DIVIDERS]\n" \
                    ";;Name           Elevation  Diverted Link    Type       Parameters\n" \
                    ";;-------------- ---------- ---------------- ---------- ----------\n" \
                    "10               0          *                CUTOFF     0          0          0\n" \
                    "NODE10   0      LK1    WEIR   0.5   2   0.7    2    0     0"
        section_from_text = self.project_reader.read_dividers.read(source_text)
        actual_text = self.project_writer.write_dividers.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match_keyword_lines(source_text, actual_text,
                                            keywords_=None, skipped_keywords=None, ignore_trailing_0=True), msg)
        # self.assertTrue(match(actual_text, source_text), msg)


def main():
    unittest.main()

if __name__ == "__main__":
    main()