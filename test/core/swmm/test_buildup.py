import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match
from core.swmm.quality import Buildup


class SingleBuildupTest(unittest.TestCase):
    """Test BUILDUP section"""

    def test_buildup(self):
        """Test all options of one Buildup type in SWMM5.1"""
        self.my_options = Buildup()
        test_text = "Residential    TSS   SAT   50   0    2   AREA "
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

    def test_buildup_section(self):
        """Test BUILDUP section using Project class"""
        from_text = Project()
        # source_text = '\n'.join(self.TEST_TEXT)
        test_text = "[BUILDUP]\n" \
                      ";;LandUse          Pollutant        Function   Coeff1   Coeff2   Coeff3   Normalizer\n" \
                      ";;-----------------------------------------------------------------------------------\n" \
                      "  Residential      TSS              SAT        50       0        2        AREA\n" \
                      "  Residential      Lead             NONE       0        0        0        AREA\n" \
                      "  Undeveloped      TSS              SAT        100      0        3        AREA\n" \
                      "  Undeveloped      Lead             NONE       0        0        0        AREA"

        from_text.set_text(test_text)
        project_section = from_text.buildup
        actual_text = project_section.get_text()
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(project_section.matches(test_text), msg)
