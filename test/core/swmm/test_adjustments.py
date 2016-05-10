from core.swmm.climatology.climatology import Adjustments
import unittest


class ClimatologyAdjustmentsTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = Adjustments()


    def runTest(self):

        # Test default, default is empty string, no adjustments
        name = self.my_options.SECTION_NAME
        assert name == "[ADJUSTMENTS]"
        actual_text = self.my_options.get_text()
        assert actual_text == ''

        # Test all options with Example 1g in SWMM 5.1.
        # 20160412xw: Example 1g appears odd. The first data column should have same meaning as the rests
        #     but the person created the test may have messed up its values.
        test_all_ops = r"""
        [ADJUSTMENTS]
        ;;Parameter  Monthly Adjustments
        TEMPERATURE    1      0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0
        EVAPORATION    2      0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0
        RAINFALL       3      1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0
        CONDUCTIVITY   4      1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0
        """
        # Test set_text
        self.my_options.set_text(test_all_ops)
        # Test get_text through matches
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_all_ops)

        # Edge Case 1: Missing a column - did not pass
        # xw: since these are optional, I assume it is acceptable to not having all columns.
        # not clear in 5.1 manual, may need to confirm with EPA?
        test_missing_col = r"""
        [ADJUSTMENTS]
        ;;Parameter  Monthly Adjustments
        TEMPERATURE    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0
        EVAPORATION    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0
        RAINFALL       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0
        CONDUCTIVITY   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0
        """
        # Test set_text
        self.my_options.set_text(test_missing_col)
        # Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_missing_col), \
            "When a column is missing in monthly ADJUSTMENTS (no column for December) it does not match"

        # Edge Case 2: Missing a row - did not pass
        # xw: since these are optional, I assume it is acceptable to not having all rows.
        # not clear in 5.1 manual, may need to confirm with EPA?
        test_missing_row = r"""
        [ADJUSTMENTS]
        ;;Parameter  Monthly Adjustments
        TEMPERATURE    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0
        RAINFALL       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0
        CONDUCTIVITY   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0
        """
        # Test set_text
        self.my_options.set_text(test_missing_row)
        # Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_missing_row), "When EVAPORATION is omitted in ADJUSTMENTS, does not match"

