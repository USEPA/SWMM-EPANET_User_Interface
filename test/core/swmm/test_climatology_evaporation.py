from core.swmm.climatology.climatology import Evaporation
import unittest


class ClimatologyEvaporationTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = Evaporation()

    def runTest(self):

        # Test default, default is empty string, no evaporation
        # -- Failed because [EVAPORATION] always written regardless of inputs
        name = self.my_options.SECTION_NAME
        assert name == "[EVAPORATION]"
        actual_text = self.my_options.get_text()
        #assert actual_text == ''

        # Test constant without DRY_ONLY
        # -- Failed because DRY_ONLY is always written regardless of inputs
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
        assert self.my_options.matches(test_constant_wo_dryonly)

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
        assert self.my_options.matches(test_monthly)

        # Test TimeSeries
        # -- Test TimeSeries first

        # Test Temperature
        # -- Test Temperature first

        # Test File
        # -- Test File, file or pan coefficient? Not quite clear based on the manual

        # Test Recovery
        # -- pattern ID, need an example. Not quite clear based on the manual


