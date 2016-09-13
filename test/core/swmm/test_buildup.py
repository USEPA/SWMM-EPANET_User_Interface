import unittest
from core.swmm.quality import Buildup
from core.swmm.inp_reader_sections import BuildupReader
from core.swmm.inp_writer_sections import BuildupWriter
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit


class SingleBuildupTest(unittest.TestCase):
    """Test BUILDUP section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_buildup(self):
        """Test all options of one Buildup type in SWMM5.1"""
        test_text = "Residential    TSS   SAT   50   0    2   AREA "
        my_options = BuildupReader.read(test_text)
        actual_text = BuildupWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_buildup_section(self):
        """Test BUILDUP section using Project class"""
        source_text = "[BUILDUP]\n" \
                      ";;LandUse          Pollutant        Function   Coeff1   Coeff2   Coeff3   Normalizer\n" \
                      ";;-----------------------------------------------------------------------------------\n" \
                      "  Residential      TSS              SAT        50       0        2        AREA\n" \
                      "  Residential      Lead             NONE       0        0        0        AREA\n" \
                      "  Undeveloped      TSS              SAT        100      0        3        AREA\n" \
                      "  Undeveloped      Lead             NONE       0        0        0        AREA"
        section_from_text = self.project_reader.read_buildup.read(source_text)
        actual_text = self.project_writer.write_buildup.as_text(section_from_text)
        msg = '\nSet:' + source_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, source_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()