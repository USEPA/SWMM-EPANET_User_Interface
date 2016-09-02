import unittest
from core.swmm.hydrology.subcatchment import Coverage
from core.swmm.hydrology.subcatchment import Coverages
from core.swmm.inp_reader_sections import CoverageReader
from core.swmm.inp_writer_sections import CoveragesWriter
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit


class SimpleCoverageTest(unittest.TestCase):
    """Test COVERAGES section"""

    def test_coverage(self):
        """Test one set of Coverage parameters from Example 5"""
        # --It seems that Coverage class is not used, only Coverages
        test_text = "S2      Residential_1    27"
        my_options = CoverageReader.read(test_text)
        assert my_options.subcatchment_name == 'S2'
        assert my_options.land_use_name == 'Residential_1'
        assert my_options.percent_subcatchment_area == '27'
        actual_text = CoveragesWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_default_coverages(self):
        """Test default, empty string wo section name"""
        my_options = Coverages()
        name = my_options.SECTION_NAME
        assert name == "[COVERAGES]"
        actual_text = CoveragesWriter.as_text(my_options)
        test_text = ""
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_coverages(self):
        """Test aquifer parameters in Example 5"""
        test_text = r"""
        [COVERAGES]
        ;;Subcatchment   Land Use         Percent
        ;;-------------- ---------------- ----------
        S1               Residential_1    100
        S2               Residential_1    27
        S2               Residential_2    73
        S3               Residential_1    27
        S3               Residential_2    32
        S4               Residential_1    9
        S4               Residential_2    30
        S4               Commercial       26
        S5               Commercial       98
        S6               Commercial       100
        """
        my_options = CoverageReader.read(test_text)
        actual_text = CoveragesWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
