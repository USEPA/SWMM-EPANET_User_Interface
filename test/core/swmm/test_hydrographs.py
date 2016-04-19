from core.inputfile import Section
from core.swmm.project import Project
from core.swmm.hydrology.unithydrograph import UnitHydrograph
import unittest

class SingleHydrographTest(unittest.TestCase):

    def setUp(self):
        self.my_options = UnitHydrograph()

    def runTest(self):
        # Test Example in SWMM 5.1 manual
        test_text = r"""UH101 RG1
                        UH101 ALL SHORT 0.033 1.0 2.0
                        UH101 ALL MEDIUM 0.300 3.0 2.0
                        UH101 ALL LONG 0.033 10.0 2.0
                        UH101 JUL SHORT 0.033 0.5 2.0
                        UH101 JUL MEDIUM 0.011 2.0 2.0
                    """
        # Test set_text
        self.my_options.set_text(test_text)
        # Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

class SimpleHydrographsTest(unittest.TestCase):

    TEST_TEXT = ("[HYDROGRAPHS]",
                 ";;Hydrograph\tMonth\tResponse\tR\tT\tK\tDmax\tDrecov\tDinit",
                 "UH101 RG1",
                 "UH101 ALL SHORT 0.033 1.0 2.0",
                 "UH101 ALL MEDIUM 0.300 3.0 2.0\t1\t2\t3",
                 "UH101 ALL LONG 0.033 10.0 2.0",
                 "UH101 JUL SHORT 0.033 0.5 2.0",
                 "UH101 JUL MEDIUM 0.011 2.0 2.0")

    def runTest(self):
        from_text = Project()
        source_text = '\n'.join(self.TEST_TEXT)
        from_text.set_text(source_text)
        project_hydrographs = from_text.hydrographs

        assert Section.match_omit(project_hydrographs.get_text(), source_text, " \t-;\n")

        assert len(project_hydrographs.value) == 1

        val = project_hydrographs.value[0]

        assert val.group_name == "UH101"
        assert val.rain_gage_id == "RG1"
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