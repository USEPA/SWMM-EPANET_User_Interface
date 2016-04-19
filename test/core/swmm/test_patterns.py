from core.swmm.patterns import Pattern
import unittest


class SinglePatternTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Pattern()

    def runTest(self):

        # Test examples

        # -- Daily total 7 per week
        test_text = r"""D1 DAILY 1.0   1.0   1.0   1.0   1.0   0.5   0.5"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        # -- Monthly total 12 per year
        test_text = r"""
        x                MONTHLY    1.0   1.0   1.0   1.0   1.0   1.0
        x                           1.0   1.0   1.0   1.0   1.0   1.0"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        # -- Hourly total 24 per day
        test_text = r"""
        DWF              HOURLY     .0151 .01373 .01812 .01098 .01098 .01922
        DWF                         .02773 .03789 .03515 .03982 .02059 .02471
        DWF                         .03021 .03789 .03350 .03158 .03954 .02114
        DWF                         .02801 .03680 .02911 .02334 .02499 .02718"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        # -- Weekend total 24 per day
        test_text = r"""
        DWF              WEEKEND     .0151 .01373 .01812 .01098 .01098 .01922
        DWF                         .02773 .03789 .03515 .03982 .02059 .02471
        DWF                         .03021 .03789 .03350 .03158 .03954 .02114
        DWF                         .02801 .03680 .02911 .02334 .02499 .02718"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        # -- Design pattern, no flag
        test_text = r"""
 1               	1.34        	1.94        	1.46        	1.44        	.76         	.92
 1               	.85         	1.07        	.96         	1.1         	1.08        	1.19
 1               	1.16        	1.08        	.96         	.83         	.79         	.74
 1               	.64         	.64         	.85         	.96         	1.24        	1.67"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        pass

class MultiInflowsTest(unittest.TestCase):

    def setUp(self):

        self.my_options = Pattern()

    def runTest(self):

        test_text = r"""
[PATTERNS]
;;Name           Type       Multipliers
;;-------------- ---------- -----------
;xx
x                MONTHLY    1.0   1.0   1.0   1.0   1.0   1.0
x                           1.0   1.0   1.0   1.0   1.0   1.0

[PATTERNS]
;;Name             Type       Multipliers
;;----------------------------------------------------------------------
  DWF              HOURLY     .0151 .01373 .01812 .01098 .01098 .01922
  DWF                         .02773 .03789 .03515 .03982 .02059 .02471
  DWF                         .03021 .03789 .03350 .03158 .03954 .02114
  DWF                         .02801 .03680 .02911 .02334 .02499 .02718

[PATTERNS]
;ID              	Multipliers
;Demand Pattern
 1               	1.0         	1.2         	1.4         	1.6         	1.4         	1.2
 1               	1.0         	0.8         	0.6         	0.4         	0.6         	0.8
        """

        # Test Net 2
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


        pass