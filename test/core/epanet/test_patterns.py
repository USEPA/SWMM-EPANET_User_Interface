import unittest
from core.epanet import patterns
from core.epanet.inp_reader_sections import PatternReader
from core.epanet.inp_writer_sections import PatternWriter
from core.epanet.epanet_project import EpanetProject
from core.epanet.inp_reader_project import InputFileReader


class SimplePatternTest(unittest.TestCase):
    """Test one pattern"""

    def setUp(self):
        """Set up test"""

    def test_pattern(self):
        """Test one pattern based on EPANET2 manual"""
        self.my_options = patterns.Pattern()
        # Test created based on manual
        # Multiple lines
        # will rewrite string to three rows each with 6, 6, 3 numbers.
        # So to compare I stripped P1, space, and \n
        test_text = "P1\t1.2\t1.4\t1.6\t1.8\t2.0\n" \
                    "P1\t2.2\t2.4\t2.6\t2.8\t3.0\n" \
                    "P1\t3.2\t3.4\t3.6\t3.8\t4.0"
        self.my_options = PatternReader.read(test_text)
        new_test = test_text.replace(' ','').replace('\n','').replace('P1','')
        actual_text = self.my_options.get_text().replace(' ','').replace('\n','').replace('P1','')
        self.assertEquals(actual_text, new_test)

    def test_patterns(self):
        """Test one Pattern section"""
        self.my_pattern = patterns.Pattern()
        self.my_pattern.description = "test pattern"
        self.my_pattern.pattern_id = "XXX"
        self.my_pattern.multipliers = ("1.0", "1.1", "1.2", "1.3")

        assert self.my_pattern.pattern_id == "XXX"
        assert self.my_pattern.description == "test pattern"
        assert PatternWriter().as_text(self.my_pattern).split() ==\
               [";test", "pattern", "XXX", "1.0", "1.1", "1.2", "1.3"], "get_text"

        # Create new Project with this section populated from TEST_TEXT
        test_text = ("[PATTERNS]",
                     ";ID\tMultipliers",
                     ";Demand Pattern",
                     " 1\t1.0\t1.2\t1.4\t1.6\t1.4\t1.2",
                     " 1\t1.0\t0.8\t0.6\t0.4\t0.6\t0.8",
                     " 2\t2.0\t2.2\t2.4\t2.6\t2.4\t2.2",
                     " 2\t2.0\t2.8\t2.6\t2.4\t2.6\t2.8")

        from_text = InputFileReader().set_from_text_lines(test_text)  # TODO: does this tuple work as iterator?
        pattern_list = from_text.patterns.value
        assert len(pattern_list) == 2
        assert int(pattern_list[0].pattern_id) == 1
        assert int(pattern_list[1].pattern_id) == 2

        assert float(pattern_list[0].multipliers[0]) == 1.0
        assert float(pattern_list[0].multipliers[1]) == 1.2
        assert float(pattern_list[0].multipliers[2]) == 1.4
        assert float(pattern_list[0].multipliers[3]) == 1.6
        assert float(pattern_list[0].multipliers[4]) == 1.4
        assert float(pattern_list[0].multipliers[5]) == 1.2

        assert float(pattern_list[0].multipliers[6]) == 1.0
        assert float(pattern_list[0].multipliers[7]) == 0.8
        assert float(pattern_list[0].multipliers[8]) == 0.6
        assert float(pattern_list[0].multipliers[9]) == 0.4
        assert float(pattern_list[0].multipliers[10]) == 0.6
        assert float(pattern_list[0].multipliers[11]) == 0.8

        assert float(pattern_list[1].multipliers[0]) == 2.0
        assert float(pattern_list[1].multipliers[1]) == 2.2
        assert float(pattern_list[1].multipliers[2]) == 2.4
        assert float(pattern_list[1].multipliers[3]) == 2.6
        assert float(pattern_list[1].multipliers[4]) == 2.4
        assert float(pattern_list[1].multipliers[5]) == 2.2

        assert float(pattern_list[1].multipliers[6]) == 2.0
        assert float(pattern_list[1].multipliers[7]) == 2.8
        assert float(pattern_list[1].multipliers[8]) == 2.6
        assert float(pattern_list[1].multipliers[9]) == 2.4
        assert float(pattern_list[1].multipliers[10]) == 2.6
        assert float(pattern_list[1].multipliers[11]) == 2.8

if __name__ == '__main__':
    my_test = SimplePatternTest()
    my_test.setUp()
    my_test.test_pattern()
    my_test.test_patterns()


