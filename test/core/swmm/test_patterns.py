import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from core.swmm.patterns import Pattern, PatternType
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class SimplePatternTest(unittest.TestCase):
    """Test PATTERNS section"""
    SOURCE_TEXTS = [
    "[PATTERNS]\n"
    ";;Name           Type       Multipliers\n"
    ";;-------------- ---------- -----------\n"
    ";xx\n"
    "x                MONTHLY    1.0   1.0   1.0   1.0   1.0   1.0\n"
    "x                           1.0   1.0   1.0   1.0   1.0   1.0",
    "[PATTERNS]\n"
    ";;Name             Type       Multipliers\n"
    ";;----------------------------------------------------------------------\n"
    "DWF              HOURLY     .0151 .01373 .01812 .01098 .01098 .01922\n"
    "DWF                         .02773 .03789 .03515 .03982 .02059 .02471\n"
    "DWF                         .03021 .03789 .03350 .03158 .03954 .02114\n"
    "DWF                         .02801 .03680 .02911 .02334 .02499 .02718"]


    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_daily(self):
        """Test Pattern: Daily total 7 per week"""
        test_text = "D1\tDAILY\t1.0\t1.0\t1.0\t1.0\t1.0\t0.5\t0.5"
        my_options = PatternReader.read(test_text)
        actual_text = PatternWriter.as_text(my_options)
        temp_pattern = PatternReader.read(actual_text)
        for item in (my_options, temp_pattern):
            assert item.name == 'D1'
            assert item.pattern_type == PatternType.DAILY
            assert ' '.join(item.multipliers) == '1.0 1.0 1.0 1.0 1.0 0.5 0.5'

    def test_monthly(self):
        """Test Pattern: Monthly total 12 per year"""
        test_text = "M1\tMONTHLY\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\n" \
                    "M1\t\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0"
        my_options = PatternReader.read(test_text)
        actual_text = PatternWriter.as_text(my_options)
        temp_pattern = PatternReader.read(actual_text)
        for item in (my_options, temp_pattern):
            assert item.name == 'M1'
            assert item.pattern_type == PatternType.MONTHLY
            assert ' '.join(item.multipliers) == '1.0 1.0 1.0 1.0 1.0 1.0 '\
                                                 '1.0 1.0 1.0 1.0 1.0 1.0'

    def test_hourly(self):
        """Test Pattern: Hourly total 24 per year"""
        test_text = r"""
        DWF              HOURLY     .0151 .01373 .01812 .01098 .01098 .01922
        DWF                         .02773 .03789 .03515 .03982 .02059 .02471
        DWF                         .03021 .03789 .03350 .03158 .03954 .02114
        DWF                         .02801 .03680 .02911 .02334 .02499 .02718"""
        my_options = PatternReader.read(test_text)
        actual_text = PatternWriter.as_text(my_options)
        temp_pattern = PatternReader.read(actual_text)
        for item in (my_options, temp_pattern):
            assert item.name == 'DWF'
            assert item.pattern_type == PatternType.HOURLY
            assert ' '.join(item.multipliers) == ".0151 .01373 .01812 .01098 .01098 .01922 "\
                                                 ".02773 .03789 .03515 .03982 .02059 .02471 "\
                                                 ".03021 .03789 .03350 .03158 .03954 .02114 "\
                                                 ".02801 .03680 .02911 .02334 .02499 .02718"
    def test_weekly(self):
        """Test Pattern: Weekend total 24 per day"""
        test_text = r"""
        DWF              WEEKEND     .0151 .01373 .01812 .01098 .01098 .01922
        DWF                         .02773 .03789 .03515 .03982 .02059 .02471
        DWF                         .03021 .03789 .03350 .03158 .03954 .02114
        DWF                         .02801 .03680 .02911 .02334 .02499 .02718"""
        my_options = PatternReader.read(test_text)
        actual_text = PatternWriter.as_text(my_options)
        temp_pattern = PatternReader.read(actual_text)
        for item in (my_options, temp_pattern):
            assert item.name == 'DWF'
            assert item.pattern_type == PatternType.WEEKEND
            assert ' '.join(item.multipliers) == ".0151 .01373 .01812 .01098 .01098 .01922 "\
                                                 ".02773 .03789 .03515 .03982 .02059 .02471 "\
                                                 ".03021 .03789 .03350 .03158 .03954 .02114 "\
                                                 ".02801 .03680 .02911 .02334 .02499 .02718"

    def test_design(self):
        """Test Pattern: Design pattern, no flag"""
        test_text = r"""
 1               	1.34        	1.94        	1.46        	1.44        	.76         	.92
 1               	.85         	1.07        	.96         	1.1         	1.08        	1.19
 1               	1.16        	1.08        	.96         	.83         	.79         	.74
 1               	.64         	.64         	.85         	.96         	1.24        	1.67"""
        my_options = PatternReader.read(test_text)
        actual_text = PatternWriter.as_text(my_options)
        temp_pattern = PatternReader.read(actual_text)
        for item in (my_options, temp_pattern):
            assert item.name == '1'
            assert ' '.join(item.multipliers) == "1.34 1.94 1.46 1.44 .76 .92 "\
                                                 ".85 1.07 .96 1.1 1.08 1.19 "\
                                                 "1.16 1.08 .96 .83 .79 .74 "\
                                                 ".64 .64 .85 .96 1.24 1.67"

    def test_pattern_section(self):
        """test PATTERNS section"""

        for source_text in self.SOURCE_TEXTS:
            section_from_text = self.project_reader.read_patterns.read(source_text)
            actual_text = self.project_writer.write_patterns.as_text(section_from_text)
            msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
            self.assertTrue(match(actual_text, source_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
