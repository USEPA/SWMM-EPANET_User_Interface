import unittest
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from core.swmm.inp_reader_sections import UnitHydrographReader
from core.swmm.inp_writer_sections import UnitHydrographWriter
from test.core.section_match import match, match_omit
from core.swmm.hydrology.unithydrograph import UnitHydrograph


class SimpleHydrographsTest(unittest.TestCase):

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_hydrograph(self):
        """Test one hydrograph based on SWMM 5.1 manual"""
        self.my_options = UnitHydrograph()
        test_text = "UH101\tRG1\n" \
                    "UH101\tALL\tSHORT\t0.033\t1.0\t2.0\t0.033\t1.0\t2.0\n" \
                    "UH101\tALL\tMEDIUM\t0.300\t3.0\t2.0\t0.033\t1.0\t2.0\n" \
                    "UH101\tALL\tLONG\t0.033\t10.0\t2.0\t0.033\t1.0\t2.0\n" \
                    "UH101\tJUL\tSHORT\t0.033\t0.5\t2.0\t0.033\t1.0\t2.0\n" \
                    "UH101\tJUL\tMEDIUM\t0.011\t2.0\t2.0\t0.033\t1.0\t2.0"
        my_options = UnitHydrographReader.read(test_text)
        actual_text = UnitHydrographWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_hydrographs(self):
        """Test HYDROGRAPHS section"""
        TEST_TEXT = ("[HYDROGRAPHS]",
                     ";;Hydrograph\tMonth\tResponse\tR\tT\tK\tDmax\tDrecov\tDinit",
                     "UH101 RG1",
                     "UH101 ALL SHORT 0.033 1.0 2.0",
                     "UH101 ALL MEDIUM 0.300 3.0 2.0\t1\t2\t3",
                     "UH101 ALL LONG 0.033 10.0 2.0",
                     "UH101 JUL SHORT 0.033 0.5 2.0",
                     "UH101 JUL MEDIUM 0.011 2.0 2.0")

        source_text = '\n'.join(TEST_TEXT)
        section_from_text = self.project_reader.read_hydrographs.read(source_text)
        actual_text = self.project_writer.write_hydrographs.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        msg += "\nxw09/01/2016: Difference in first comment line Month vs. Rain Gage/Month"
        self.assertTrue(match_omit(actual_text, source_text, " \t-;\n"), msg)

        assert len(section_from_text.value) == 1

        val = section_from_text.value[0]

        assert val.name == "UH101"
        assert val.rain_gage_name == "RG1"
        assert len(val.value) == 5

        hydrograph_item = val.value[0]
        assert hydrograph_item.hydrograph_month == "ALL"
        assert hydrograph_item.term == "SHORT"
        assert hydrograph_item.response_ratio == "0.033"
        assert hydrograph_item.time_to_peak == "1.0"
        assert hydrograph_item.recession_limb_ratio == "2.0"
        assert hydrograph_item.initial_abstraction_depth == ''
        assert hydrograph_item.initial_abstraction_rate == ''
        assert hydrograph_item.initial_abstraction_amount == ''

        hydrograph_item = val.value[1]
        assert hydrograph_item.hydrograph_month == "ALL"
        assert hydrograph_item.term == "MEDIUM"
        assert hydrograph_item.response_ratio == "0.300"
        assert hydrograph_item.time_to_peak == "3.0"
        assert hydrograph_item.recession_limb_ratio == "2.0"
        assert hydrograph_item.initial_abstraction_depth == '1'
        assert hydrograph_item.initial_abstraction_rate == '2'
        assert hydrograph_item.initial_abstraction_amount == '3'

        hydrograph_item = val.value[2]
        assert hydrograph_item.hydrograph_month == "ALL"
        assert hydrograph_item.term == "LONG"
        assert hydrograph_item.response_ratio == "0.033"
        assert hydrograph_item.time_to_peak == "10.0"
        assert hydrograph_item.recession_limb_ratio == "2.0"
        assert hydrograph_item.initial_abstraction_depth == ''
        assert hydrograph_item.initial_abstraction_rate == ''
        assert hydrograph_item.initial_abstraction_amount == ''

        hydrograph_item = val.value[4]
        assert hydrograph_item.hydrograph_month == "JUL"
        assert hydrograph_item.term == "MEDIUM"
        assert hydrograph_item.response_ratio == "0.011"
        assert hydrograph_item.time_to_peak == "2.0"
        assert hydrograph_item.recession_limb_ratio == "2.0"
        assert hydrograph_item.initial_abstraction_depth == ''
        assert hydrograph_item.initial_abstraction_rate == ''
        assert hydrograph_item.initial_abstraction_amount == ''

def main():
    unittest.main()

if __name__ == "__main__":
    main()
