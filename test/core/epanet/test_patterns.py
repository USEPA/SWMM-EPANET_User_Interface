import unittest
from core.epanet import patterns
from core.epanet.inp_reader_sections import PatternReader
from core.epanet.inp_writer_sections import PatternWriter
from core.epanet.inp_reader_project import InputFileReader
from core.epanet.inp_reader_project import ProjectReader
from core.epanet.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit


class SimplePatternTest(unittest.TestCase):
    """Test one pattern"""

    TEST_TEXTS = [["P1\t1.2\t1.4\t1.6\t1.8\t2.0\n" \
                   "P1\t2.2\t2.4\t2.6\t2.8\t3.0\n" \
                   "P1\t3.2\t3.4\t3.6\t3.8\t4.0",
                   "P1",
                   ['1.2', '1.4', '1.6', '1.8', '2.0', '2.2', '2.4', '2.6', '2.8', '3.0', '3.2', '3.4', '3.6', '3.8', '4.0']],
                  ["P2\t1.2\t1.4\t1.6\t1.8\t2.0\t2.1\n" \
                   "P2\t2.2\t2.4\t2.6\t2.8\t3.0\t3.1\n" \
                   "P2\t3.2\t3.4\t3.6\t3.8\t4.0\t4.1",
                   "P2",
                   ['1.2', '1.4', '1.6', '1.8', '2.0', '2.1', '2.2', '2.4', '2.6', '2.8', '3.0', '3.1', '3.2', '3.4', '3.6', '3.8','4.0', '4.1']]
                  ]

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_pattern(self):
        """Test one pattern based on EPANET2 manual"""
        # Test created based on manual
        # Multiple lines
        # will rewrite string to three rows each with 6, 6, 3 numbers.
        # So to compare I stripped P1, space, and \n
        for test_text in self.TEST_TEXTS:
            my_options = PatternReader.read(test_text[0])
            assert my_options.name == test_text[1]
            assert my_options.multipliers == test_text[2]
            # actual_text = PatternWriter.as_text(my_options)
            # msg = '\nSet:\n'+test_text+'\nGet:\n'+actual_text
            # self.assertTrue(match(actual_text, test_text), msg)

    def test_patterns(self):
        """Test one Pattern section"""
        # Create new Project with this section populated from TEST_TEXT
        test_text = ("[PATTERNS]",
                     ";ID\tMultipliers",
                     ";Demand Pattern",
                     " 1\t1.0\t1.2\t1.4\t1.6\t1.4\t1.2",
                     " 1\t1.0\t0.8\t0.6\t0.4\t0.6\t0.8",
                     " 2\t2.0\t2.2\t2.4\t2.6\t2.4\t2.2",
                     " 2\t2.0\t2.8\t2.6\t2.4\t2.6\t2.8")
        source_text = "\n".join(test_text)
        section_from_text = self.project_reader.read_patterns.read(source_text)
        actual_text = self.project_writer.write_patterns.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match(actual_text, source_text), msg)

        pattern_list = section_from_text
        assert len(pattern_list.value) == 2
        assert int(pattern_list.value[0].name) == 1
        assert int(pattern_list.value[1].name) == 2

        assert float(pattern_list.value[0].multipliers[0]) == 1.0
        assert float(pattern_list.value[0].multipliers[1]) == 1.2
        assert float(pattern_list.value[0].multipliers[2]) == 1.4
        assert float(pattern_list.value[0].multipliers[3]) == 1.6
        assert float(pattern_list.value[0].multipliers[4]) == 1.4
        assert float(pattern_list.value[0].multipliers[5]) == 1.2

        assert float(pattern_list.value[0].multipliers[6]) == 1.0
        assert float(pattern_list.value[0].multipliers[7]) == 0.8
        assert float(pattern_list.value[0].multipliers[8]) == 0.6
        assert float(pattern_list.value[0].multipliers[9]) == 0.4
        assert float(pattern_list.value[0].multipliers[10]) == 0.6
        assert float(pattern_list.value[0].multipliers[11]) == 0.8

        assert float(pattern_list.value[1].multipliers[0]) == 2.0
        assert float(pattern_list.value[1].multipliers[1]) == 2.2
        assert float(pattern_list.value[1].multipliers[2]) == 2.4
        assert float(pattern_list.value[1].multipliers[3]) == 2.6
        assert float(pattern_list.value[1].multipliers[4]) == 2.4
        assert float(pattern_list.value[1].multipliers[5]) == 2.2

        assert float(pattern_list.value[1].multipliers[6]) == 2.0
        assert float(pattern_list.value[1].multipliers[7]) == 2.8
        assert float(pattern_list.value[1].multipliers[8]) == 2.6
        assert float(pattern_list.value[1].multipliers[9]) == 2.4
        assert float(pattern_list.value[1].multipliers[10]) == 2.6
        assert float(pattern_list.value[1].multipliers[11]) == 2.8

def main():
    unittest.main()

if __name__ == "__main__":
    main()
# if __name__ == '__main__':
#     my_test = SimplePatternTest()
#     my_test.setUp()
#     my_test.test_pattern()
#     my_test.test_patterns()


