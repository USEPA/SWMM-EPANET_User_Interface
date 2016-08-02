import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match
from core.swmm.patterns import Pattern, PatternType


class SimplePatternTest(unittest.TestCase):
    """Test PATTERNS section"""

    def test_daily(self):
        """Test Pattern: Daily total 7 per week"""
        self.my_options = Pattern()
        temp_pattern = Pattern()  # This is used to create a copy of each test using set_text and get_text to test both
        test_text = "D1\tDAILY\t1.0\t1.0\t1.0\t1.0\t1.0\t0.5\t0.5"
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        temp_pattern.set_text(self.my_options.get_text())
        for item in (self.my_options, temp_pattern):
            assert item.name == 'D1'
            assert item.pattern_type == PatternType.DAILY
            assert ' '.join(item.multipliers) == '1.0 1.0 1.0 1.0 1.0 0.5 0.5'

    def test_monthly(self):
        """Test Pattern: Monthly total 12 per year"""
        self.my_options = Pattern()
        temp_pattern = Pattern()  # This is used to create a copy of each test using set_text and get_text to test both
        test_text = "M1\tMONTHLY\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0\n" \
                    "M1\t\t1.0\t1.0\t1.0\t1.0\t1.0\t1.0"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()
        new_text = actual_text.replace(" ", "")
        temp_pattern.set_text(self.my_options.get_text())
        for item in (self.my_options, temp_pattern):
            assert item.name == 'M1'
            assert item.pattern_type == PatternType.MONTHLY
            assert ' '.join(item.multipliers) == '1.0 1.0 1.0 1.0 1.0 1.0 '\
                                                 '1.0 1.0 1.0 1.0 1.0 1.0'

    def test_hourly(self):
        """Test Pattern: Hourly total 24 per year"""
        self.my_options = Pattern()
        temp_pattern = Pattern()  # This is used to create a copy of each test using set_text and get_text to test both
        test_text = r"""
        DWF              HOURLY     .0151 .01373 .01812 .01098 .01098 .01922
        DWF                         .02773 .03789 .03515 .03982 .02059 .02471
        DWF                         .03021 .03789 .03350 .03158 .03954 .02114
        DWF                         .02801 .03680 .02911 .02334 .02499 .02718"""
        # --Test set_text
        self.my_options.set_text(test_text)
        temp_pattern.set_text(self.my_options.get_text())
        for item in (self.my_options, temp_pattern):
            assert item.name == 'DWF'
            assert item.pattern_type == PatternType.HOURLY
            assert ' '.join(item.multipliers) == ".0151 .01373 .01812 .01098 .01098 .01922 "\
                                                 ".02773 .03789 .03515 .03982 .02059 .02471 "\
                                                 ".03021 .03789 .03350 .03158 .03954 .02114 "\
                                                 ".02801 .03680 .02911 .02334 .02499 .02718"
    def test_weekly(self):
        """Test Pattern: Weekend total 24 per day"""
        self.my_options = Pattern()
        temp_pattern = Pattern()  # This is used to create a copy of each test using set_text and get_text to test both
        test_text = r"""
        DWF              WEEKEND     .0151 .01373 .01812 .01098 .01098 .01922
        DWF                         .02773 .03789 .03515 .03982 .02059 .02471
        DWF                         .03021 .03789 .03350 .03158 .03954 .02114
        DWF                         .02801 .03680 .02911 .02334 .02499 .02718"""
        # --Test set_text
        self.my_options.set_text(test_text)
        temp_pattern.set_text(self.my_options.get_text())
        for item in (self.my_options, temp_pattern):
            assert item.name == 'DWF'
            assert item.pattern_type == PatternType.WEEKEND
            assert ' '.join(item.multipliers) == ".0151 .01373 .01812 .01098 .01098 .01922 "\
                                                 ".02773 .03789 .03515 .03982 .02059 .02471 "\
                                                 ".03021 .03789 .03350 .03158 .03954 .02114 "\
                                                 ".02801 .03680 .02911 .02334 .02499 .02718"

    def test_design(self):
        """Test Pattern: Design pattern, no flag"""
        self.my_options = Pattern()
        temp_pattern = Pattern()  # This is used to create a copy of each test using set_text and get_text to test both
        test_text = r"""
 1               	1.34        	1.94        	1.46        	1.44        	.76         	.92
 1               	.85         	1.07        	.96         	1.1         	1.08        	1.19
 1               	1.16        	1.08        	.96         	.83         	.79         	.74
 1               	.64         	.64         	.85         	.96         	1.24        	1.67"""

        # --Test set_text
        self.my_options.set_text(test_text)
        temp_pattern.set_text(self.my_options.get_text())
        for item in (self.my_options, temp_pattern):
            assert item.name == '1'
            assert ' '.join(item.multipliers) == "1.34 1.94 1.46 1.44 .76 .92 "\
                                                 ".85 1.07 .96 1.1 1.08 1.19 "\
                                                 "1.16 1.08 .96 .83 .79 .74 "\
                                                 ".64 .64 .85 .96 1.24 1.67"

    def test_pattern_section(self):
        """test PATTERNS section"""
        test_text = r"""
[PATTERNS]
;;Name           Type       Multipliers
;;-------------- ---------- -----------
;xx
x                MONTHLY    1.0   1.0   1.0   1.0   1.0   1.0
x                           1.0   1.0   1.0   1.0   1.0   1.0"""
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.patterns
        assert match_omit(project_section.get_text(), test_text, " \t-;\n")

        test_text=r"""[PATTERNS]
;;Name             Type       Multipliers
;;----------------------------------------------------------------------
  DWF              HOURLY     .0151 .01373 .01812 .01098 .01098 .01922
  DWF                         .02773 .03789 .03515 .03982 .02059 .02471
  DWF                         .03021 .03789 .03350 .03158 .03954 .02114
  DWF                         .02801 .03680 .02911 .02334 .02499 .02718"""
        test_text = """
[PATTERNS]
;ID              	Multipliers
;Demand Pattern
 1               	1.0         	1.2         	1.4         	1.6         	1.4         	1.2
 1               	1.0         	0.8         	0.6         	0.4         	0.6         	0.8
        """

        test_text = """[PATTERNS]
;ID              	Multipliers
;Demand Pattern
 1               	1.26        	1.04        	.97         	.97         	.89         	1.19
 1               	1.28        	.67         	.67         	1.34        	2.46        	.97
 1               	.92         	.68         	1.43        	.61         	.31         	.78
 1               	.37         	.67         	1.26        	1.56        	1.19        	1.26
 1               	.6          	1.1         	1.03        	.73         	.88         	1.06
 1               	.99         	1.72        	1.12        	1.34        	1.12        	.97
 1               	1.04        	1.15        	.91         	.61         	.68         	.46
 1               	.51         	.74         	1.12        	1.34        	1.26        	.97
 1               	.82         	1.37        	1.03        	.81         	.88         	.81
 1               	.81
;Pump Station Outflow Pattern
 2               	.96         	.96         	.96         	.96         	.96         	.96
 2               	.62         	0           	0           	0           	0           	0
 2               	.8          	1           	1           	1           	1           	.15
 2               	0           	0           	0           	0           	0           	0
 2               	.55         	.92         	.92         	.92         	.92         	.9
 2               	.9          	.45         	0           	0           	0           	0
 2               	0           	.7          	1           	1           	1           	1
 2               	.2          	0           	0           	0           	0           	0
 2               	0           	.74         	.92         	.92         	.92         	.92
 2               	.92
;Pump Station Fluoride Pattern
 3               	.98         	1.02        	1.05        	.99         	.64         	.46
 3               	.35         	.35         	.35         	.35         	.35         	.35
 3               	.17         	.17         	.13         	.13         	.13         	.15
 3               	.15         	.15         	.15         	.15         	.15         	.15
 3               	.15         	.12         	.1          	.08         	.11         	.09
 3               	.09         	.08         	.08         	.08         	.08         	.08
 3               	.08         	.09         	.07         	.07         	.09         	.09
 3               	.09         	.09         	.09         	.09         	.09         	.09
 3               	.09         	.08         	.35         	.72         	.82         	.92
 3               	1
"""
        # Test Net 3
        test_text = """[PATTERNS]
;ID              	Multipliers
;General Default Demand Pattern
 1               	1.34        	1.94        	1.46        	1.44        	.76         	.92
 1               	.85         	1.07        	.96         	1.1         	1.08        	1.19
 1               	1.16        	1.08        	.96         	.83         	.79         	.74
 1               	.64         	.64         	.85         	.96         	1.24        	1.67
;Demand Pattern for Node 123
 2               	0           	0           	0           	0           	0           	1219
 2               	0           	0           	0           	1866        	1836        	1818
 2               	1818        	1822        	1822        	1817        	1824        	1816
 2               	1833        	1817        	1830        	1814        	1840        	1859
;Demand Pattern for Node 15
 3               	620         	620         	620         	620         	620         	360
 3               	360         	0           	0           	0           	0           	360
 3               	360         	360         	360         	360         	0           	0
 3               	0           	0           	0           	0           	360         	360
;Demand Pattern for Node 35
 4               	1637        	1706        	1719        	1719        	1791        	1819
 4               	1777        	1842        	1815        	1825        	1856        	1801
 4               	1819        	1733        	1664        	1620        	1613        	1620
 4               	1616        	1647        	1627        	1627        	1671        	1668
;Demand Pattern for Node 203
 5               	4439        	4531        	4511        	4582        	4531        	4582
 5               	4572        	4613        	4643        	4643        	4592        	4613
 5               	4531        	4521        	4449        	4439        	4449        	4460
 5               	4439        	4419        	4368        	4399        	4470        	4480
"""
