import unittest
from core.swmm.climatology import Adjustments
from core.swmm.inp_reader_sections import AdjustmentsReader
from core.swmm.inp_writer_sections import AdjustmentsWriter
from test.core.section_match import match, match_omit


class AdjustmentsTest(unittest.TestCase):
    """Test ADJUSTMENT section in climatology"""

    def test_default(self):
        """Test default, default is empty string, no adjustments"""
        my_options = Adjustments()
        name = my_options.SECTION_NAME
        assert name == "[ADJUSTMENTS]"
        actual_text = AdjustmentsWriter.as_text(my_options)
        assert actual_text == ""

    def test_all_opts(self):
        """Test all options with Example 1g in SWMM 5.1.
        20160412xw: Example 1g appears odd. The first data
                column should have same meaning as the rests
        but the person created the test may have messed up its values. """
        test_text = r"""
        [ADJUSTMENTS]
        ;;Parameter  Monthly Adjustments
        TEMPERATURE    1      0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0
        EVAPORATION    2      0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0
        RAINFALL       3      1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0
        CONDUCTIVITY   4      1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0
        """
        # Test set_text
        my_options = AdjustmentsReader.read(test_text)
        actual_text = AdjustmentsWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_miss_col(self):
        """Edge Case 1: Missing a column - did not pass, expected to fail.
        xw: since these are optional, I assume it is acceptable to not having all columns.
                not clear in 5.1 manual, may need to confirm with EPA?"""
        test_text = r"""
        [ADJUSTMENTS]
        ;;Parameter  Monthly Adjustments
        TEMPERATURE    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0
        EVAPORATION    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0
        RAINFALL       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0
        CONDUCTIVITY   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0
        """
        # Test set_text
        my_options = AdjustmentsReader.read(test_text)
        actual_text = AdjustmentsWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertFalse(match(actual_text, test_text), \
            "When a column is missing in monthly ADJUSTMENTS (no column for December) it does not match")

    def test_miss_row(self):
        """Edge Case 2: Missing a row - did not pass, expected to fail
         xw: since these are optional, I assume it is acceptable to not having all rows.
         not clear in 5.1 manual, may need to confirm with EPA? """
        test_text = r"""
        [ADJUSTMENTS]
        ;;Parameter  Monthly Adjustments
        TEMPERATURE    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0    0.0
        RAINFALL       1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0
        CONDUCTIVITY   1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0    1.0
        """
        my_options = AdjustmentsReader.read(test_text)
        actual_text = AdjustmentsWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertFalse(match(actual_text, test_text), \
                          "When EVAPORATION is omitted in ADJUSTMENTS, does not match")

def main():
    unittest.main()

if __name__ == "__main__":
    main()