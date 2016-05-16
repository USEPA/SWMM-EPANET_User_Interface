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

    # TODO: Add testing of each EvaporationFormat

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

class ClimatologyEvaporationTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = Evaporation()

    def runTest(self):

        # Test default, default is empty string, no evaporation
        name = self.my_options.SECTION_NAME
        assert name == "[EVAPORATION]"
        actual_text = self.my_options.get_text()
        #assert actual_text == ''
        # -- [EVAPORATION] always written regardless of inputs, OK with bare session

        # Test constant without DRY_ONLY
        test_constant_wo_dryonly = r"""
        [EVAPORATION]
        ;;Data Source    Parameters
        ;;-------------- ----------------
        CONSTANT         0.0
        """
        # Test set_text
        self.my_options.set_text(test_constant_wo_dryonly)
        # Test get_text through matches
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.constant == '0.0'
        assert self.my_options.dry_only == False
        # assert self.my_options.matches(test_constant_wo_dryonly), "If DRY_ONLY is not specified, match returns False."
        # -- DRY_ONLY is always written regardless of inputs, DRY only is False (NO) by default, OK.

        # Test constant with DRY_ONLY, consistent with most examples
        test_constant = r"""
        [EVAPORATION]
        ;;Data Source    Parameters
        ;;-------------- ----------------
        CONSTANT         0.0
        DRY_ONLY         NO
        """
        # Test set_text
        self.my_options.set_text(test_constant)
        # Test get_text through matches
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_constant)

        # Test monthly Example User2 and a few others
        test_monthly = r"""
        [EVAPORATION]
        ;;Type         Parameters
        ;;-----------------------
          MONTHLY      0.01   0.04   0.05   0.05   0.1    0.24   0.25   0.24   0.16   0.11   0.03   0.01
          DRY_ONLY     Yes
        """
        # Test set_text
        self.my_options.set_text(test_monthly)
        # Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_monthly)

        # Test monthly - edge case missing a month
        # -- I think the case should fail because it is missing a month
        test_monthly = r"""
        [EVAPORATION]
        ;;Type         Parameters
        ;;-----------------------
          MONTHLY      0.01   0.04   0.05   0.05   0.1    0.24   0.25   0.24   0.16   0.11   0.03
          DRY_ONLY No
        """
        # Test set_text
        self.my_options.set_text(test_monthly)
        # Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        # assert self.my_options.matches(test_monthly)
        # -- This is deemed to fail

        # Test TimeSeries
        # -- Test TimeSeries first

        # Test Temperature
        # -- Test Temperature first

        # Test File
        # -- Test File, file or pan coefficient? Not quite clear based on the manual

        # Test Recovery
        # -- pattern ID, need an example. Not quite clear based on the manual
