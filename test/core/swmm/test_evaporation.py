from core.inputfile import Section
from core.swmm.project import Project
from core.swmm.climatology.climatology import EvaporationFormat
from core.swmm.climatology.climatology import Evaporation
import unittest


class SimpleEvaporationTest(unittest.TestCase):
    TEST_TEXT_CONSTANT = ("[EVAPORATION]",
                          ";;Type      \tParameters",
                          ";;----------\t----------",
                          "CONSTANT    \t0.2",
                          "DRY_ONLY    \tNO")

    def runTest(self):
        from_text = Project()
        source_text = '\n'.join(self.TEST_TEXT_CONSTANT)
        from_text.set_text(source_text)
        project_section = from_text.evaporation

        assert Section.match_omit(project_section.get_text(), source_text, " \t-;\n")
        assert project_section.format == EvaporationFormat.CONSTANT
        assert project_section.constant == "0.2"
        assert project_section.monthly == ()
        assert project_section.timeseries == ''
        assert project_section.monthly_pan_coefficients == ()
        assert project_section.recovery_pattern == ''
        assert project_section.dry_only is False


# TODO: Add testing of each EvaporationFormat -- added xwei 5/19/2016
class EvaporationTest(unittest.TestCase):
    """Test all options provided in EVAPORATION section"""

    # preparing to test
    def setUp(self):
        """ Setting up for the test """

    # testing bare section
    def test_bare(self):
        """testing bare section"""
        self.my_options = Evaporation()
        # default is empty string, no evaporation
        name = self.my_options.SECTION_NAME
        assert name == "[EVAPORATION]"
        actual_text = self.my_options.get_text()
        assert actual_text == ''
        # -- [EVAPORATION] always written regardless of inputs, OK with bare session

    # testing constant only
    def test_constant_only(self):
        """testing constant only without DRY_ONLY"""
        self.my_options = Evaporation()
        test_text = "[EVAPORATION]\n" \
                    ";;Data Source    Parameters\n" \
                    ";;-------------- ----------------\n" \
                    " CONSTANT         0.0"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.constant == '0.0'
        assert self.my_options.dry_only == False
        # assert self.my_options.matches(test_constant_wo_dryonly),
        # "If DRY_ONLY is not specified, match returns False."
        # -- DRY_ONLY is always written regardless of inputs
        # DRY only is False (NO) by default, OK.

    # testing constant with DRY_ONLY option
    def test_constant_wt_dry_only(self):
        """Test constant with DRY_ONLY, consistent with most examples"""
        self.my_options = Evaporation()
        test_constant = "[EVAPORATION]\n" \
                        ";;Data Source    Parameters\n" \
                        ";;-------------- ----------------\n" \
                        " CONSTANT         0.0\n" \
                        " DRY_ONLY         NO"
        self.my_options.set_text(test_constant)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_constant)

    def test_monthly(self):
        """Test monthly Example User2 and a few others"""
        self.my_options = Evaporation()
        test_monthly = "[EVAPORATION]\n" \
                       ";;Type         Parameters\n" \
                       ";;-----------------------\n" \
                       "MONTHLY      0.01   0.04   0.05   0.05   0.1    0.24" \
                       "   0.25   0.24   0.16   0.11   0.03   0.01\n" \
                       "DRY_ONLY     Yes"
        self.my_options.set_text(test_monthly)
        # Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_monthly)

    # Test monthly - edge case missing a month
    def test_monthly_fail(self):
        """MONTHLY - edge case missing a month"""
        # -- I think the case should fail because it is missing a month
        # -- Currently do not have the missing value detection ability
        self.my_options = Evaporation()
        test_monthly = "[EVAPORATION]\n" \
                       ";;Type         Parameters\n" \
                       ";;-----------------------\n" \
                       " MONTHLY      0.01   0.04   0.05   0.05   0.1    0.24" \
                       "   0.25   0.24   0.16   0.11   0.03\n" \
                       "DRY_ONLY No"
        self.my_options.set_text(test_monthly)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_monthly)

    # test timeseries option
    def test_timeseries(self):
        """TIMESERIES Tseries"""
        self.my_options = Evaporation()
        test_text = "[EVAPORATION]\n" \
                    ";;Type         Parameters\n" \
                    ";;-----------------------\n" \
                    "TIMESERIES TS1"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

    # test temperature option
    def test_temperature(self):
        """TEMPERATURE"""
        self.my_options = Evaporation()
        test_text = "[EVAPORATION]\n" \
                    ";;Type         Parameters\n" \
                    ";;-----------------------\n" \
                    "TEMPERATURE"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

    # test file option
    def test_file(self):
        """FILE"""
        self.my_options = Evaporation()
        test_text = "[EVAPORATION]\n" \
                    ";;Type         Parameters\n" \
                    ";;-----------------------\n" \
                    "FILE"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

    # test recovery option
    def test_recovery(self):
        """RECOVERY PatternID"""
        self.my_options = Evaporation()
        test_text = "[EVAPORATION]\n" \
                    ";;Type         Parameters\n" \
                    ";;-----------------------\n" \
                    "RECOVERY  pattern1"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)


if __name__ == '__main__':
    # Creating a new test suite
    my_suite = unittest.TestSuite()

    # Adding a test case
    my_suite.addTest(unittest.makeSuite(EvaporationTest))

    # Adding a specific function
    my_suite.addTest(EvaporationTest("test_bare"))
    my_suite.addTest(EvaporationTest("test_constant_only"))
    my_suite.addTest(EvaporationTest("test_constant_wt_dry_only"))
    my_suite.addTest(EvaporationTest("test_monthly"))
    my_suite.addTest(EvaporationTest("test_monthly_fail"))
    my_suite.addTest(EvaporationTest("test_timeseries"))
    my_suite.addTest(EvaporationTest("test_temperature"))
    my_suite.addTest(EvaporationTest("test_file"))
    my_suite.addTest(EvaporationTest("test_recovery"))

    # Running the tests
    testRunner = unittest.TextTestRunner()
    testRunner.run(my_suite)

